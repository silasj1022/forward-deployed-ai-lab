"""HTTP routes for the public demo and automation clients."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from fastapi import APIRouter, HTTPException, Request

from ..agents.registry import agent_registry
from ..evaluation.benchmark import run_benchmark
from ..evaluation.red_team import run_red_team
from ..integrations import integration_catalog
from ..models.domain import AssistRequest, AssistResponse, ProposedAction
from .schemas import ApprovalDecisionRequest, HealthResponse

if TYPE_CHECKING:
    from ..app import ApplicationContainer

router = APIRouter(prefix="/api/v1")


def _container(request: Request) -> ApplicationContainer:
    return cast("ApplicationContainer", request.app.state.container)


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    container = _container(request)
    return HealthResponse(
        status="ok",
        environment=container.settings.environment,
        model_provider=container.model_provider.name,
        integrations={
            "salesforce_mode": "live" if container.salesforce.live else "synthetic",
            "audit_chain": container.audit_logger.verify_chain(),
        },
    )


@router.post("/assist", response_model=AssistResponse)
def assist(payload: AssistRequest, request: Request) -> AssistResponse:
    return _container(request).orchestrator.run(payload)


@router.get("/approvals/{approval_id}")
def get_approval(approval_id: str, request: Request) -> dict[str, Any]:
    record = _container(request).approvals.get(approval_id)
    if not record:
        raise HTTPException(status_code=404, detail="Approval not found")
    return record


@router.post("/approvals/{approval_id}/decision")
def decide_approval(
    approval_id: str,
    payload: ApprovalDecisionRequest,
    request: Request,
) -> dict[str, Any]:
    container = _container(request)
    try:
        record = container.approvals.decide(
            approval_id,
            approved=payload.approved,
            decided_by=payload.decided_by,
            comment=payload.comment,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Approval not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    execution: dict[str, Any] | None = None
    if payload.approved and payload.execute_synthetic_action:
        action = ProposedAction.model_validate(record["action"])
        try:
            execution = container.salesforce.execute_case_update(action, approved=True)
        except (KeyError, PermissionError) as exc:
            execution = {"success": False, "error": str(exc)}
    container.audit_logger.append(
        "approval.decided",
        {"approval": record, "execution": execution},
    )
    return {"approval": record, "execution": execution}


@router.post("/evaluations/benchmark")
def benchmark(request: Request) -> dict[str, Any]:
    container = _container(request)
    return run_benchmark(
        container.orchestrator,
        golden_set_path=Path(container.settings.data_dir) / "eval/golden_set.json",
        output_path=Path(container.settings.artifact_dir) / "evaluation-report.json",
        enable_mlflow=container.settings.enable_mlflow,
    )


@router.post("/evaluations/red-team")
def red_team(request: Request) -> dict[str, Any]:
    container = _container(request)
    return run_red_team(
        container.orchestrator,
        prompts_path=Path(container.settings.data_dir) / "red_team/prompts.json",
        output_path=Path(container.settings.artifact_dir) / "red-team-report.json",
    )


@router.get("/architecture/capabilities")
def capabilities() -> dict[str, Any]:
    return {"agents": agent_registry(), "integrations": integration_catalog()}
