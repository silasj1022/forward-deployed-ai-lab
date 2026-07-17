"""Cross-platform evidence metadata for versioned JSON datasets."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


def canonical_json_sha256(value: Any) -> str:
    """Hash JSON semantics rather than platform-specific newline bytes."""
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def dataset_label(path: Path) -> str:
    """Return a stable path beginning at the nearest data directory."""
    parts = path.parts
    data_indexes = [index for index, part in enumerate(parts) if part == "data"]
    selected = parts[data_indexes[-1] :] if data_indexes else (path.name,)
    return PurePosixPath(*selected).as_posix()
