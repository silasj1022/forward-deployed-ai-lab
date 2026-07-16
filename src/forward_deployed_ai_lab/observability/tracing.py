"""Stage-level timing and trace collection."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from time import perf_counter
from typing import Any

from ..models.domain import TraceStep


class TraceRecorder:
    def __init__(self) -> None:
        self.steps: list[TraceStep] = []

    @contextmanager
    def stage(self, name: str, detail: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        started_at = datetime.now(UTC)
        started = perf_counter()
        mutable_detail = dict(detail or {})
        status = "ok"
        try:
            yield mutable_detail
        except Exception as exc:
            status = "error"
            mutable_detail["error_type"] = type(exc).__name__
            raise
        finally:
            completed_at = datetime.now(UTC)
            self.steps.append(
                TraceStep(
                    stage=name,
                    status=status,
                    started_at=started_at,
                    completed_at=completed_at,
                    latency_ms=round((perf_counter() - started) * 1000, 3),
                    detail=mutable_detail,
                )
            )
