#!/usr/bin/env python3
"""Fail fast when the public portfolio tree or checked-in evidence is incomplete."""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "pyproject.toml",
    "requirements.txt",
    ".env.example",
    ".devcontainer/devcontainer.json",
    ".github/workflows/ci.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/release.yml",
    "src/forward_deployed_ai_lab/agents/orchestrator.py",
    "src/forward_deployed_ai_lab/tools/salesforce.py",
    "src/forward_deployed_ai_lab/evaluation/benchmark.py",
    "tests/test_orchestrator.py",
    "scripts/installed_package_smoke.py",
    "data/eval/golden_set.json",
    "data/red_team/prompts.json",
    "artifacts/evaluation-report.json",
    "artifacts/red-team-report.json",
    "docs/evidence-index.md",
    "docs/system-card.md",
    "docs/framework-strategy.md",
    "docs/evaluation-strategy.md",
    "docs/deep-research-roadmap.md",
    "docs/repository-settings-checklist.md",
]


def read_json(relative_path: str) -> dict[str, Any]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def file_sha256(relative_path: str) -> str:
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def project_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject["project"]["version"])


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).is_file()]
    if missing:
        print("Repository integrity check failed. Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    evaluation = read_json("artifacts/evaluation-report.json")
    red_team = read_json("artifacts/red-team-report.json")
    eval_metrics = evaluation.get("metrics", {})
    red_metrics = red_team.get("metrics", {})
    version = project_version()

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    if pyproject["project"]["name"] != "enterprise-agent-foundry":
        print("Package metadata does not use the Enterprise Agent Foundry name.")
        return 1
    init_source = (ROOT / "src/forward_deployed_ai_lab/__init__.py").read_text(
        encoding="utf-8"
    )
    version_match = re.search(r'^__version__ = "([^"]+)"$', init_source, re.MULTILINE)
    if version_match is None or version_match.group(1) != version:
        print("Package runtime version does not match pyproject.toml.")
        return 1
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if 'title: "Enterprise Agent Foundry"' not in citation:
        print("Citation metadata does not use the Enterprise Agent Foundry name.")
        return 1
    mojibake_markers = ("Â", "Ã", "â€", "â†")
    text_paths = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
    corrupted = [
        str(path.relative_to(ROOT))
        for path in text_paths
        if any(marker in path.read_text(encoding="utf-8") for marker in mojibake_markers)
    ]
    if corrupted:
        print(f"Encoding artifact check failed: {corrupted}")
        return 1

    expected = {
        "project_version": version,
        "golden_schema": "1.1",
        "golden_dataset_sha256": file_sha256("data/eval/golden_set.json"),
        "golden_case_count": 10,
        "golden_gate": 1.0,
        "red_schema": "1.1",
        "red_dataset_sha256": file_sha256("data/red_team/prompts.json"),
        "red_team_case_count": 8,
        "red_team_gate": 1.0,
        "source_coverage_metric_present": True,
    }
    actual = {
        "project_version": evaluation.get("project_version"),
        "golden_schema": evaluation.get("schema_version"),
        "golden_dataset_sha256": evaluation.get("dataset_sha256"),
        "golden_case_count": eval_metrics.get("case_count")
        if isinstance(eval_metrics, dict)
        else None,
        "golden_gate": eval_metrics.get("quality_gate_pass_rate")
        if isinstance(eval_metrics, dict)
        else None,
        "red_schema": red_team.get("schema_version"),
        "red_dataset_sha256": red_team.get("dataset_sha256"),
        "red_team_case_count": red_metrics.get("case_count")
        if isinstance(red_metrics, dict)
        else None,
        "red_team_gate": red_metrics.get("pass_rate") if isinstance(red_metrics, dict) else None,
        "source_coverage_metric_present": (
            "mean_retrieved_source_coverage_proxy" in eval_metrics
            if isinstance(eval_metrics, dict)
            else False
        ),
    }
    if actual != expected:
        print("Evidence consistency check failed.")
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        return 1

    print(f"Repository integrity verified: {len(REQUIRED_PATHS)} required files present.")
    print(f"Checked-in evidence verified for project version {version}.")
    print("Dataset hashes, 10 golden cases, and 8 red-team cases are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
