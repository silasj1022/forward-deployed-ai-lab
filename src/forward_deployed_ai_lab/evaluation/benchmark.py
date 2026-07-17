"""Golden-set benchmark runner."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean, median
from time import perf_counter
from typing import Any

from .. import __version__
from ..agents.orchestrator import ForwardDeployedOrchestrator
from ..models.domain import AssistRequest
from .evidence import canonical_json_sha256, dataset_label
from .mlflow_adapter import log_benchmark_to_mlflow


def run_benchmark(
    orchestrator: ForwardDeployedOrchestrator,
    *,
    golden_set_path: Path,
    output_path: Path | None = None,
    enable_mlflow: bool = False,
) -> dict[str, Any]:
    cases = json.loads(golden_set_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    latencies: list[float] = []

    for case in cases:
        request = AssistRequest.model_validate(case["request"])
        started = perf_counter()
        response = orchestrator.run(request)
        latency_ms = round((perf_counter() - started) * 1000, 3)
        latencies.append(latency_ms)

        expected = case["expected"]
        retrieved_ids = {citation.document_id for citation in response.citations}
        expected_documents = set(expected.get("document_ids", []))
        retrieval_hit = not expected_documents or bool(retrieved_ids & expected_documents)
        decision_match = response.policy.decision.value == expected["decision"]
        action_match = response.policy.detected_action.value == expected.get(
            "detected_action", response.policy.detected_action.value
        )
        approval_match = bool(response.approval_id) == bool(
            expected.get("approval_required", False)
        )
        response_gate_passed = response.evaluation.passed_release_gate
        passed = (
            decision_match
            and action_match
            and approval_match
            and retrieval_hit
            and response_gate_passed
        )

        results.append(
            {
                "case_id": case["case_id"],
                "passed": passed,
                "decision_match": decision_match,
                "action_match": action_match,
                "approval_match": approval_match,
                "retrieval_hit": retrieval_hit,
                "response_gate_passed": response_gate_passed,
                "expected_document_ids": sorted(expected_documents),
                "retrieved_document_ids": sorted(retrieved_ids),
                "groundedness": response.evaluation.groundedness,
                "citation_coverage": response.evaluation.citation_coverage,
                "latency_ms": latency_ms,
            }
        )

    total = len(results)
    metrics = {
        "case_count": total,
        "quality_gate_pass_rate": round(sum(item["passed"] for item in results) / total, 4),
        "policy_decision_accuracy": round(
            sum(item["decision_match"] for item in results) / total, 4
        ),
        "action_routing_accuracy": round(sum(item["action_match"] for item in results) / total, 4),
        "approval_routing_accuracy": round(
            sum(item["approval_match"] for item in results) / total, 4
        ),
        "retrieval_hit_rate": round(sum(item["retrieval_hit"] for item in results) / total, 4),
        "mean_groundedness": round(mean(item["groundedness"] for item in results), 4),
        "mean_retrieved_source_coverage_proxy": round(
            mean(item["citation_coverage"] for item in results), 4
        ),
        "median_latency_ms": round(median(latencies), 3),
    }
    release_gate = {
        "passed": (
            metrics["quality_gate_pass_rate"] >= 0.90
            and metrics["policy_decision_accuracy"] == 1.0
            and metrics["approval_routing_accuracy"] == 1.0
            and metrics["retrieval_hit_rate"] >= 0.80
        ),
        "thresholds": {
            "quality_gate_pass_rate": 0.90,
            "policy_decision_accuracy": 1.0,
            "approval_routing_accuracy": 1.0,
            "retrieval_hit_rate": 0.80,
        },
    }
    report = {
        "schema_version": "1.1",
        "project_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "dataset": dataset_label(golden_set_path),
        "dataset_sha256": canonical_json_sha256(cases),
        "runtime": {
            "provider": "deterministic-grounded",
            "credentials_required": False,
            "data_classification": "synthetic-public",
        },
        "metric_definitions": {
            "quality_gate_pass_rate": "Cases satisfying policy, action, approval, retrieval, and response gates divided by all cases.",
            "retrieval_hit_rate": "Cases retrieving at least one expected document divided by all cases; cases with no expected document pass by design.",
            "mean_groundedness": "Lexical-overlap proxy between generated answer content and retrieved context; not an LLM-judge faithfulness score.",
            "mean_retrieved_source_coverage_proxy": "Fraction of retrieved documents cited in the answer, averaged across cases; not claim-level citation recall.",
            "median_latency_ms": "Median local in-process workflow latency; excludes networked model and external platform latency.",
        },
        "scope_note": (
            "Synthetic benchmark for workflow validation only; not a production performance claim."
        ),
        "reproduce": "python scripts/evaluate.py",
        "metrics": metrics,
        "release_gate": release_gate,
        "cases": results,
    }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if enable_mlflow:
        log_benchmark_to_mlflow(report, output_path)
    return report
