"""Validated runtime configuration.

Secrets are loaded from environment variables or a local .env file. The public
repository never contains live credentials.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with a single FDAI_ environment-variable prefix."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="FDAI_",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Forward-Deployed AI Delivery Lab"
    environment: Literal["local", "test", "staging", "production"] = "local"
    host: str = "0.0.0.0"
    port: int = Field(default=3000, ge=1, le=65535)
    log_level: str = "INFO"

    data_dir: Path = Path("data")
    artifact_dir: Path = Path("artifacts")
    audit_log_path: Path = Path("logs/audit.jsonl")

    model_provider: Literal[
        "deterministic", "openai", "anthropic", "azure", "bedrock", "vertex"
    ] = "deterministic"
    model_name: str = "offline-grounded-demo"
    top_k: int = Field(default=3, ge=1, le=10)
    minimum_groundedness: float = Field(default=0.35, ge=0.0, le=1.0)

    enable_langgraph: bool = False
    enable_mlflow: bool = False
    enable_opentelemetry: bool = False
    mlflow_tracking_uri: str = "file:./mlruns"
    mlflow_experiment: str = "forward-deployed-ai-lab"

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    azure_ai_endpoint: str | None = None
    azure_ai_api_key: str | None = None
    aws_region: str = "us-east-1"
    google_cloud_project: str | None = None

    salesforce_instance_url: str | None = None
    salesforce_access_token: str | None = None
    salesforce_api_version: str = "v61.0"
    allow_salesforce_writes: bool = False
    live_integrations_enabled: bool = False

    def ensure_runtime_directories(self) -> None:
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_runtime_directories()
    return settings
