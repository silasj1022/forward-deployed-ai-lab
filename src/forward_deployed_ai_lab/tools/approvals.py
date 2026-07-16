"""Human-approval registry for consequential actions."""

from __future__ import annotations

import hashlib
import json
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

    @staticmethod
    def action_hash(action: ProposedAction) -> str:
        """Bind approval and execution to the exact proposed action."""
        payload = action.model_dump(mode="json", exclude={"status"})
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def create(self, action: ProposedAction, *, trace_id: str) -> str:
        approval_id = new_id("apr")
        action_hash = self.action_hash(action)
        with self._lock:
            self._records[approval_id] = {
                "approval_id": approval_id,
                "trace_id": trace_id,
                "status": "pending",
                "action": action.model_dump(mode="json"),
                "action_hash": action_hash,
                "idempotency_key": f"{approval_id}:{action_hash}",
                "created_at": datetime.now(UTC).isoformat(),
                "decided_at": None,
                "decided_by": None,
                "comment": None,
                "execution_status": "not_started",
                "execution_attempts": 0,
                "execution_result": None,
                "execution_error": None,
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
            desired_status = "approved" if approved else "rejected"
            if record["status"] != "pending":
                same_decision = (
                    record["status"] == desired_status
                    and record["decided_by"] == decided_by
                    and record["comment"] == comment
                )
                if not same_decision:
                    raise ValueError("Approval has already been decided differently")
                replay = dict(record)
                replay["decision_replayed"] = True
                return replay
            record["status"] = desired_status
            record["decided_at"] = datetime.now(UTC).isoformat()
            record["decided_by"] = decided_by
            record["comment"] = comment
            decided = dict(record)
            decided["decision_replayed"] = False
            return decided

    def claim_execution(
        self, approval_id: str, action: ProposedAction
    ) -> tuple[bool, dict[str, Any] | None, str]:
        """Claim a bound action once, or return its prior successful result."""
        with self._lock:
            record = self._records.get(approval_id)
            if record is None:
                raise KeyError(approval_id)
            if record["status"] != "approved":
                raise PermissionError("The action does not have an approved decision")
            if record["action_hash"] != self.action_hash(action):
                raise PermissionError("The approved action no longer matches the proposed action")
            if record["execution_status"] == "succeeded":
                result = record["execution_result"]
                return False, dict(result) if isinstance(result, dict) else None, str(
                    record["idempotency_key"]
                )
            if record["execution_status"] == "in_progress":
                raise ValueError("The approved action is already being executed")
            record["execution_status"] = "in_progress"
            record["execution_attempts"] = int(record["execution_attempts"]) + 1
            record["execution_error"] = None
            return True, None, str(record["idempotency_key"])

    def complete_execution(self, approval_id: str, result: dict[str, Any]) -> None:
        with self._lock:
            record = self._records[approval_id]
            record["execution_status"] = "succeeded"
            record["execution_result"] = dict(result)

    def fail_execution(self, approval_id: str, error: str) -> None:
        with self._lock:
            record = self._records[approval_id]
            record["execution_status"] = "failed"
            record["execution_error"] = error
