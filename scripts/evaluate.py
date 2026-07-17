#!/usr/bin/env python3
"""Run the synthetic golden-set benchmark."""

from pathlib import Path

from forward_deployed_ai_lab.app import build_container
from forward_deployed_ai_lab.evaluation import run_benchmark


def main() -> None:
    container = build_container()
    report = run_benchmark(
        container.orchestrator,
        golden_set_path=container.settings.resolved_data_dir / "eval/golden_set.json",
        output_path=Path(container.settings.artifact_dir) / "evaluation-report.json",
        enable_mlflow=container.settings.enable_mlflow,
    )
    print(report["metrics"])
    if not report["release_gate"]["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
