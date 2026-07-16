"""Typed domain models shared by the API, workflow, and evaluation layers."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Decision(StrEnum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionKind(StrEnum):
    READ = "read"
    UPDATE_CASE = "update_case"
    CLOSE_CASE = "close_case"
    CREATE_REFUND = "create_refund"
    DELETE_DATA = "delete_data"
    ESCALATE = "escalate"
    NONE = "none"


class KnowledgeDocument(BaseModel):
    document_id: str
    title: str
    content: str
    source: str
    tags: list[str] = Field(default_factory=list)
    allowed_roles: list[str] = Field(default_factory=lambda: ["agent", "manager", "admin"])
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedDocument(KnowledgeDocument):
    score: float = Field(ge=0.0)


class Citation(BaseModel):
    document_id: str
    title: str
    source: str
    excerpt: str
    score: float = Field(ge=0.0)


class PolicyDecision(BaseModel):
    decision: Decision
    risk_level: RiskLevel
    reasons: list[str]
    controls: list[str] = Field(default_factory=list)
    requires_human_approval: bool = False
    detected_action: ActionKind = ActionKind.NONE


class ProposedAction(BaseModel):
    action_id: str
    kind: ActionKind
    target: str
    payload: dict[str, Any]
    rationale: str
    status: str = "pending"


class TraceStep(BaseModel):
    stage: str
    status: str
    started_at: datetime
    completed_at: datetime
    latency_ms: float = Field(ge=0.0)
    detail: dict[str, Any] = Field(default_factory=dict)


class EvaluationSummary(BaseModel):
    groundedness: float = Field(ge=0.0, le=1.0)
    citation_coverage: float = Field(ge=0.0, le=1.0)
    policy_consistency: float = Field(ge=0.0, le=1.0)
    passed_release_gate: bool


class AssistRequest(BaseModel):
    query: str = Field(min_length=3, max_length=4000)
    user_role: str = "agent"
    case_id: str | None = None
    requested_action: ActionKind = ActionKind.NONE
    metadata: dict[str, Any] = Field(default_factory=dict)


class AssistResponse(BaseModel):
    trace_id: str
    answer: str
    policy: PolicyDecision
    citations: list[Citation]
    proposed_action: ProposedAction | None = None
    approval_id: str | None = None
    evaluation: EvaluationSummary
    trace: list[TraceStep]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
