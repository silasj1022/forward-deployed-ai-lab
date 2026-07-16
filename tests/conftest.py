from pathlib import Path

import pytest

from forward_deployed_ai_lab.app import build_container
from forward_deployed_ai_lab.config import Settings


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    project_root = Path(__file__).resolve().parents[1]
    return Settings(
        environment="test",
        data_dir=project_root / "data",
        artifact_dir=tmp_path / "artifacts",
        audit_log_path=tmp_path / "logs/audit.jsonl",
        model_provider="deterministic",
        top_k=3,
    )


@pytest.fixture()
def container(settings: Settings):
    return build_container(settings)
