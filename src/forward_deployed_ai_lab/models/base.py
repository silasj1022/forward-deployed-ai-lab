"""Model-provider protocol."""

from __future__ import annotations

from typing import Protocol

from .domain import KnowledgeDocument


class ModelProvider(Protocol):
    name: str
    prompt_version: str

    def generate(
        self,
        *,
        query: str,
        documents: list[KnowledgeDocument],
        case_context: dict[str, object] | None = None,
    ) -> str:
        """Generate a response grounded in supplied documents and context."""
