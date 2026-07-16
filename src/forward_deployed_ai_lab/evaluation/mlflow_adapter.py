"""Optional MLflow experiment tracking."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def log_benchmark_to_mlflow(report: dict[str, Any], artifact_path: Path | None) -> None:
    import mlflow  # type: ignore[import-not-found]

    with mlflow.start_run(run_name="synthetic-release-gate"):
        mlflow.log_param("dataset", report["dataset"])
        for name, value in report["metrics"].items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(name, float(value))
        mlflow.log_param("release_gate_passed", report["release_gate"]["passed"])
        if artifact_path and artifact_path.exists():
            mlflow.log_artifact(str(artifact_path))
