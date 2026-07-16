"""Prompt-injection and unsafe-action red-team suite."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .. import __version__
from ..agents.orchestrator import ForwardDeployedOrchestrator
from ..models.domain import AssistRequest


def run_red_team(
    orchestrator: ForwardDeployedOrchestrator,
    *,
    prompts_path: Path,
    output_path: Path | None = None,
) -> dict[str, Any]:
    cases = json.loads(prompts_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for case in cases:
        response = orchestrator.run(AssistRequest.model_validate(case["request"]))
        expected = case["expected_decision"]
        passed = response.policy.decision.value == expected
        results.append(
            {
                "case_id": case["case_id"],
                "category": case["category"],
                "expected_decision": expected,
                "actual_decision": response.policy.decision.value,
                "passed": passed,
                "reasons": response.policy.reasons,
            }
        )
    total = len(results)
    prompts_bytes = prompts_path.read_bytes()
    report = {
        "schema_version": "1.1",
        "project_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "dataset": str(prompts_path),
        "dataset_sha256": hashlib.sha256(prompts_bytes).hexdigest(),
        "runtime": {
            "provider": "deterministic-policy-gate",
            "credentials_required": False,
            "data_classification": "synthetic-public",
        },
        "metric_definitions": {
            "pass_rate": "Cases where the actual allow/review/block decision matches the expected decision divided by all adversarial cases."
        },
        "scope_note": "Synthetic adversarial tests; extend with domain-specific threat intelligence.",
        "reproduce": "python scripts/red_team.py",
        "metrics": {
            "case_count": total,
            "pass_rate": round(sum(item["passed"] for item in results) / total, 4),
        },
        "cases": results,
    }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
