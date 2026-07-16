"""API-only request and response schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ApprovalDecisionRequest(BaseModel):
    approved: bool
    decided_by: str = Field(min_length=2, max_length=120)
    comment: str | None = Field(default=None, max_length=1000)
    execute_synthetic_action: bool = True


class HealthResponse(BaseModel):
    status: str
    environment: str
    model_provider: str
    integrations: dict[str, Any]
