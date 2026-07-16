"""Human-approval registry for consequential actions."""

from __future__ import annotations

from datetime import UTC, datetime
from threading import RLock
from typing import Any

from ..models.domain import ProposedAction
from ..utils.ids import new_id


class ApprovalStore:
    """Thread-safe in-memory approval store for the demo.

    Production deployments should use durable storage and identity-backed
    approvals. The interface is intentionally storage-agnostic.
    """

    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}
        self._lock = RLock()

    def create(self, action: ProposedAction, *, trace_id: str) -> str:
        approval_id = new_id("apr")
        with self._lock:
            self._records[approval_id] = {
                "approval_id": approval_id,
                "trace_id": trace_id,
                "status": "pending",
                "action": action.model_dump(mode="json"),
                "created_at": datetime.now(UTC).isoformat(),
                "decided_at": None,
                "decided_by": None,
                "comment": None,
            }
        return approval_id

    def get(self, approval_id: str) -> dict[str, Any] | None:
        with self._lock:
            record = self._records.get(approval_id)
            return dict(record) if record else None

    def decide(
        self,
        approval_id: str,
        *,
        approved: bool,
        decided_by: str,
        comment: str | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            if approval_id not in self._records:
                raise KeyError(approval_id)
            record = self._records[approval_id]
            if record["status"] != "pending":
                raise ValueError("Approval has already been decided")
            record["status"] = "approved" if approved else "rejected"
            record["decided_at"] = datetime.now(UTC).isoformat()
            record["decided_by"] = decided_by
            record["comment"] = comment
            return dict(record)
