"""Approved-knowledge retrieval with a dependency-free BM25 implementation."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

from ..models.domain import KnowledgeDocument, RetrievedDocument
from ..utils.text import tokenize


class KnowledgeBase:
    """Load and retrieve vetted knowledge records.

    The default BM25 backend is transparent and deterministic. A vector backend
    can replace it behind the same interface for production deployments.
    """

    def __init__(self, documents: list[KnowledgeDocument]) -> None:
        if not documents:
            raise ValueError("KnowledgeBase requires at least one document")
        self.documents = documents
        self._tokens = [tokenize(document.title + " " + document.content) for document in documents]
        self._lengths = [len(tokens) for tokens in self._tokens]
        self._average_length = sum(self._lengths) / len(self._lengths)
        self._document_frequency = self._calculate_document_frequency()

    @classmethod
    def from_json(cls, path: Path) -> KnowledgeBase:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls([KnowledgeDocument.model_validate(item) for item in payload])

    def _calculate_document_frequency(self) -> Counter[str]:
        frequencies: Counter[str] = Counter()
        for tokens in self._tokens:
            frequencies.update(set(tokens))
        return frequencies

    def retrieve(
        self, query: str, *, top_k: int = 3, user_role: str = "agent"
    ) -> list[RetrievedDocument]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        scored: list[RetrievedDocument] = []
        total_documents = len(self.documents)
        k1 = 1.5
        b = 0.75

        for document, tokens, document_length in zip(
            self.documents, self._tokens, self._lengths, strict=True
        ):
            if user_role not in document.allowed_roles:
                continue
            term_frequency = Counter(tokens)
            score = 0.0
            for term in query_tokens:
                frequency = term_frequency[term]
                if frequency == 0:
                    continue
                document_frequency = self._document_frequency[term]
                inverse_document_frequency = math.log(
                    1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5)
                )
                denominator = frequency + k1 * (
                    1 - b + b * document_length / max(self._average_length, 1.0)
                )
                score += inverse_document_frequency * (frequency * (k1 + 1)) / denominator
            if score > 0:
                scored.append(RetrievedDocument(**document.model_dump(), score=round(score, 6)))

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]
