#!/usr/bin/env python3
"""Verify an installed distribution without relying on the repository checkout."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from forward_deployed_ai_lab import __version__
from forward_deployed_ai_lab.app import create_app
from forward_deployed_ai_lab.config import Settings


def main() -> int:
    original_directory = Path.cwd()
    with tempfile.TemporaryDirectory() as temporary_directory:
        try:
            os.chdir(temporary_directory)
            settings = Settings(
                environment="test",
                artifact_dir=Path("artifacts"),
                audit_log_path=Path("logs/audit.jsonl"),
            )
            assert settings.resolved_data_dir.is_dir()
            assert settings.resolved_web_dir.is_dir()
            client = TestClient(create_app(settings))
            assert client.get("/").status_code == 200
            health = client.get("/api/v1/health")
            health.raise_for_status()
            assist = client.post(
                "/api/v1/assist",
                json={"query": "What is the P1 response target?", "requested_action": "read"},
            )
            assist.raise_for_status()
            assert assist.json()["citations"]
            benchmark = client.post("/api/v1/evaluations/benchmark")
            benchmark.raise_for_status()
            assert benchmark.json()["release_gate"]["passed"] is True
            red_team = client.post("/api/v1/evaluations/red-team")
            red_team.raise_for_status()
            assert red_team.json()["metrics"]["pass_rate"] == 1.0
            print(f"installed distribution smoke test passed for {__version__}")
        finally:
            os.chdir(original_directory)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
