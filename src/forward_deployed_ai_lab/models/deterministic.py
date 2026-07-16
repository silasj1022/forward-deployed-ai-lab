"""Credential-free response generator used by tests and the public demo."""

from __future__ import annotations

import re

from .domain import KnowledgeDocument

_SENTENCE = re.compile(r"(?<=[.!?])\s+")


class DeterministicGroundedModel:
    """Compose a transparent answer directly from retrieved source text.

    This is intentionally not presented as a production LLM. It keeps the demo
    reproducible and lets reviewers inspect the orchestration, controls, and
    evaluation layers without providing API credentials.
    """

    name = "deterministic-grounded-demo"
    prompt_version = "deterministic-grounded-v1"

    def generate(
        self,
        *,
        query: str,
        documents: list[KnowledgeDocument],
        case_context: dict[str, object] | None = None,
    ) -> str:
        if not documents:
            return (
                "I could not find an approved source that supports a reliable answer. "
                "Route this request to a human owner or add vetted knowledge before acting."
            )

        statements: list[str] = []
        for document in documents[:2]:
            sentences = [part.strip() for part in _SENTENCE.split(document.content) if part.strip()]
            if sentences:
                statements.append(sentences[0])

        context_line = ""
        if case_context:
            safe_fields = {
                key: value
                for key, value in case_context.items()
                if key in {"case_id", "subject", "status", "priority", "owner", "account_name"}
            }
            if safe_fields:
                rendered = ", ".join(f"{key}={value}" for key, value in safe_fields.items())
                context_line = f" Case context: {rendered}."

        citations = " ".join(f"[{doc.document_id}]" for doc in documents[:2])
        return f"{' '.join(statements)}{context_line} Sources: {citations}".strip()
