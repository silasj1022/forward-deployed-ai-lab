"""Evaluation, benchmarking, and red-team utilities.

Imports are lazy so the core orchestrator can use metric helpers without a
circular dependency through the benchmark runner.
"""

from __future__ import annotations

from typing import Any


def run_benchmark(*args: Any, **kwargs: Any) -> dict[str, Any]:
    from .benchmark import run_benchmark as implementation

    return implementation(*args, **kwargs)


def run_red_team(*args: Any, **kwargs: Any) -> dict[str, Any]:
    from .red_team import run_red_team as implementation

    return implementation(*args, **kwargs)


__all__ = ["run_benchmark", "run_red_team"]
