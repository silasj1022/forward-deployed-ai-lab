"""Optional LangGraph runtime with durable-state and interrupt extension points.

The main demo remains dependency-light. Install the ``agents`` extra and set
``FDAI_ENABLE_LANGGRAPH=true`` to experiment with this adapter.
"""

from __future__ import annotations

from typing import Any

from .orchestrator import ForwardDeployedOrchestrator
from .state import WorkflowState


def build_langgraph(orchestrator: ForwardDeployedOrchestrator) -> Any:
    """Build a resumable graph around the framework-neutral orchestrator.

    A production deployment would split the deterministic orchestrator stages
    into dedicated nodes and replace ``InMemorySaver`` with a durable
    checkpointer such as Postgres. The approval node demonstrates a named-human
    interrupt that resumes the same thread after a decision.
    """
    from langgraph.checkpoint.memory import InMemorySaver  # type: ignore[import-not-found]
    from langgraph.graph import END, START, StateGraph  # type: ignore[import-not-found]
    from langgraph.types import Command, interrupt  # type: ignore[import-not-found]

    from ..models.domain import AssistRequest

    def execute(state: WorkflowState) -> dict[str, Any]:
        response = orchestrator.run(AssistRequest.model_validate(state["request"]))
        return {"response": response.model_dump(mode="json")}

    def approval(state: WorkflowState) -> Any:
        response = state["response"]
        approval_id = response.get("approval_id")
        if not approval_id:
            return Command(goto="finish")
        decision = interrupt(
            {
                "approval_id": approval_id,
                "question": "Approve the proposed enterprise write?",
                "action": response.get("proposed_action"),
            }
        )
        return Command(goto="finish", update={"human_decision": decision})

    def finish(state: WorkflowState) -> dict[str, Any]:
        return dict(state)

    builder = StateGraph(WorkflowState)
    builder.add_node("execute", execute)
    builder.add_node("approval", approval)
    builder.add_node("finish", finish)
    builder.add_edge(START, "execute")
    builder.add_edge("execute", "approval")
    builder.add_edge("finish", END)
    return builder.compile(checkpointer=InMemorySaver(), name="Forward-Deployed AI Lab")
