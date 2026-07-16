"""Explicit workflow state for deterministic and LangGraph runtimes."""

from __future__ import annotations

from typing import Any, TypedDict


class WorkflowState(TypedDict, total=False):
    request: dict[str, Any]
    response: dict[str, Any]
    human_decision: dict[str, Any]
    trace_id: str
    query: str
    user_role: str
    case_id: str | None
    requested_action: str
    case_context: dict[str, Any] | None
    retrieved_documents: list[dict[str, Any]]
    policy: dict[str, Any]
    answer: str
    proposed_action: dict[str, Any] | None
    approval_id: str | None
    evaluation: dict[str, Any]
