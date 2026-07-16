import json

import pytest

from forward_deployed_ai_lab.config import Settings
from forward_deployed_ai_lab.models.providers import build_model_provider, provider_capabilities


def test_network_provider_requires_explicit_credentials(tmp_path):
    settings = Settings(
        environment="test",
        data_dir=tmp_path,
        artifact_dir=tmp_path / "artifacts",
        audit_log_path=tmp_path / "logs/audit.jsonl",
        model_provider="openai",
        openai_api_key=None,
    )
    with pytest.raises(ValueError, match="FDAI_OPENAI_API_KEY"):
        build_model_provider(settings)


def test_provider_capability_catalog_is_honest():
    capabilities = provider_capabilities()
    by_name = {item["provider"]: item for item in capabilities}
    assert by_name["deterministic"]["status"] == "implemented"
    assert by_name["openai"]["status"] == "implemented-optional"
    assert by_name["azure"]["status"] == "extension-point"
    assert json.dumps(capabilities)
