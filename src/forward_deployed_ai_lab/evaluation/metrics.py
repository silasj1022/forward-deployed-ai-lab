"""Deterministic evaluation metrics for the credential-free release gate."""

from __future__ import annotations

from collections.abc import Sequence

from ..models.domain import Decision, PolicyDecision, RetrievedDocument
from ..utils.text import lexical_overlap, tokenize

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
    "you",
}


def citation_coverage(answer: str, documents: Sequence[RetrievedDocument]) -> float:
    if not documents:
        return 1.0 if "cannot" in answer.lower() or "could not" in answer.lower() else 0.0
    cited = sum(1 for document in documents if f"[{document.document_id}]" in answer)
    return round(cited / len(documents), 4)


def groundedness(answer: str, documents: Sequence[RetrievedDocument]) -> float:
    if not documents:
        return 1.0 if "cannot" in answer.lower() else 0.0
    context = " ".join(document.content for document in documents)
    content_tokens = [token for token in tokenize(answer) if token not in STOPWORDS]
    citation_free = " ".join(token for token in content_tokens if not token.startswith("kb"))
    return round(min(lexical_overlap(citation_free, context, STOPWORDS) * 2.0, 1.0), 4)


def policy_consistency(answer: str, policy: PolicyDecision) -> float:
    lowered = answer.lower()
    if policy.decision == Decision.BLOCK:
        return 1.0 if "cannot" in lowered and "not executed" not in lowered else 0.0
    if policy.decision == Decision.REVIEW:
        return 1.0 if "not executed" in lowered and "approval" in lowered else 0.0
    return 1.0 if "sources:" in lowered else 0.0


def evaluate_response(
    *,
    answer: str,
    documents: Sequence[RetrievedDocument],
    policy: PolicyDecision,
    minimum_groundedness: float = 0.25,
) -> dict[str, float | bool]:
    evaluation_documents = [] if policy.decision == Decision.BLOCK else documents
    grounded = groundedness(answer, evaluation_documents)
    coverage = citation_coverage(answer, evaluation_documents)
    consistency = policy_consistency(answer, policy)
    passed = (
        coverage >= 0.66
        and consistency == 1.0
        and (grounded >= minimum_groundedness or policy.decision == Decision.BLOCK)
    )
    return {
        "groundedness": grounded,
        "citation_coverage": coverage,
        "policy_consistency": consistency,
        "passed_release_gate": passed,
    }
