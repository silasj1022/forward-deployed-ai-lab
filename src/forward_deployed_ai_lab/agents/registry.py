"""Inspectable agent registry used by architecture and recruiter endpoints."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    mission: str
    tools: tuple[str, ...]
    authority: str


AGENTS = (
    AgentDefinition(
        name="intake",
        mission="Normalize the customer request, identity context, and requested business action.",
        tools=("request-schema", "case-context"),
        authority="read-only",
    ),
    AgentDefinition(
        name="retrieval",
        mission="Retrieve approved enterprise knowledge with source-level traceability.",
        tools=("bm25", "vector-adapter"),
        authority="read-only",
    ),
    AgentDefinition(
        name="policy",
        mission="Detect prompt injection, restricted data requests, and consequential actions.",
        tools=("policy-engine", "risk-controls"),
        authority="block-or-route",
    ),
    AgentDefinition(
        name="response",
        mission="Generate a source-grounded answer or a transparent escalation.",
        tools=("model-provider", "citation-builder"),
        authority="draft-only",
    ),
    AgentDefinition(
        name="evaluation",
        mission="Measure groundedness, citation coverage, and release-gate compliance.",
        tools=("deterministic-metrics", "ragas-adapter", "mlflow-adapter"),
        authority="score-only",
    ),
)


def agent_registry() -> list[dict[str, object]]:
    return [asdict(agent) for agent in AGENTS]
