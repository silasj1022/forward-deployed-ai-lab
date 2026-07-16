"""Text normalization and secret-redaction helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable

TOKEN_RE = re.compile(r"[A-Za-z0-9_'-]+")
SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"\b(?:sk|rk)-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
)


def tokenize(value: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(value)]


def redact(value: str) -> str:
    output = value
    for pattern in SECRET_PATTERNS:
        output = pattern.sub("[REDACTED]", output)
    return output


def lexical_overlap(left: str, right: str, stopwords: Iterable[str] = ()) -> float:
    stop = set(stopwords)
    a = {token for token in tokenize(left) if token not in stop}
    b = {token for token in tokenize(right) if token not in stop}
    if not a:
        return 0.0
    return len(a & b) / len(a)


def redact_data(value: object) -> object:
    """Recursively redact secrets without corrupting structured JSON data."""

    if isinstance(value, str):
        return redact(value)
    if isinstance(value, dict):
        return {str(key): redact_data(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_data(item) for item in value]
    if isinstance(value, tuple):
        return [redact_data(item) for item in value]
    return value
