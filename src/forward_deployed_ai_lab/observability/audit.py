"""Append-only, hash-chained audit events with secret redaction."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from threading import RLock
from typing import Any

from ..utils.text import redact_data


class AuditLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()

    def _last_hash(self) -> str:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return "GENESIS"
        with self.path.open("rb") as handle:
            lines = handle.readlines()
        if not lines:
            return "GENESIS"
        try:
            record = json.loads(lines[-1])
        except json.JSONDecodeError:
            return "CORRUPT-PREVIOUS-RECORD"
        if not isinstance(record, dict):
            return "CORRUPT-PREVIOUS-RECORD"
        record_hash = record.get("record_hash")
        return record_hash if isinstance(record_hash, str) else "CORRUPT-PREVIOUS-RECORD"

    def append(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            previous_hash = self._last_hash()
            safe_payload = redact_data(payload)
            record = {
                "timestamp": datetime.now(UTC).isoformat(),
                "event_type": event_type,
                "payload": safe_payload,
                "previous_hash": previous_hash,
            }
            canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
            record["record_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
            return record

    def verify_chain(self) -> tuple[bool, int]:
        if not self.path.exists():
            return True, 0
        previous = "GENESIS"
        count = 0
        for line in self.path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            expected_hash = record.pop("record_hash")
            if record["previous_hash"] != previous:
                return False, count
            canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
            actual_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            if actual_hash != expected_hash:
                return False, count
            previous = expected_hash
            count += 1
        return True, count
