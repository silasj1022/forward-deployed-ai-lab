#!/usr/bin/env python3
"""Run the synthetic red-team suite."""

from pathlib import Path

from forward_deployed_ai_lab.app import build_container
from forward_deployed_ai_lab.evaluation import run_red_team


def main() -> None:
    container = build_container()
    report = run_red_team(
        container.orchestrator,
        prompts_path=container.settings.resolved_data_dir / "red_team/prompts.json",
        output_path=Path(container.settings.artifact_dir) / "red-team-report.json",
    )
    print(report["metrics"])
    if report["metrics"]["pass_rate"] != 1.0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
