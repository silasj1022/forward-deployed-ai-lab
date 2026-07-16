"""End-to-end enterprise AI workflow orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..config import Settings
from ..evaluation.metrics import evaluate_response
from ..models.base import ModelProvider
from ..models.domain import (
    ActionKind,
    AssistRequest,
    AssistResponse,
    Citation,
    Decision,
    EvaluationSummary,
    ProposedAction,
)
from ..observability import AuditLogger, TraceRecorder
from ..tools import ApprovalStore, KnowledgeBase, PolicyEngine, SalesforceClient
from ..utils.ids import new_id


@dataclass
class WorkflowDependencies:
    settings: Settings
    knowledge_base: KnowledgeBase
    policy_engine: PolicyEngine
    approvals: ApprovalStore
    salesforce: SalesforceClient
    model_provider: ModelProvider
    audit_logger: AuditLogger


class ForwardDeployedOrchestrator:
    def __init__(self, dependencies: WorkflowDependencies) -> None:
        self.deps = dependencies

    def run(self, request: AssistRequest) -> AssistResponse:
        trace_id = new_id("trace")
        trace = TraceRecorder()
        case_context: dict[str, Any] | None = None

        with trace.stage("intake", {"user_role": request.user_role}) as detail:
            detail["requested_action"] = request.requested_action.value
            detail["case_id_present"] = bool(request.case_id)

        if request.case_id:
            with trace.stage("enterprise_context", {"system": "salesforce"}) as detail:
                case_context = self.deps.salesforce.get_case(request.case_id)
                detail["record_found"] = case_context is not None
                detail["mode"] = "live" if self.deps.salesforce.live else "synthetic"

        with trace.stage("retrieval") as detail:
            documents = self.deps.knowledge_base.retrieve(
                request.query,
                top_k=self.deps.settings.top_k,
                user_role=request.user_role,
            )
            detail["document_ids"] = [document.document_id for document in documents]
            detail["top_score"] = documents[0].score if documents else 0.0

        retrieval_confidence = min(documents[0].score / 4.0, 1.0) if documents else 0.0
        with trace.stage("policy") as detail:
            policy = self.deps.policy_engine.evaluate(
                query=request.query,
                requested_action=request.requested_action,
                retrieval_confidence=retrieval_confidence,
            )
            detail["decision"] = policy.decision.value
            detail["risk_level"] = policy.risk_level.value
            detail["detected_action"] = policy.detected_action.value

        proposed_action: ProposedAction | None = None
        approval_id: str | None = None
        citations = [
            Citation(
                document_id=document.document_id,
                title=document.title,
                source=document.source,
                excerpt=document.content[:220],
                score=document.score,
            )
            for document in documents
        ]

        with trace.stage("response") as detail:
            if policy.decision == Decision.BLOCK:
                answer = (
                    "I cannot fulfill that request because it conflicts with the configured security "
                    "and data-governance boundary. I can help with a read-only summary or route the "
                    "request to an authorized human owner."
                )
                citations = []
                detail["mode"] = "safe-block"
            else:
                answer = self.deps.model_provider.generate(
                    query=request.query,
                    documents=list(documents),
                    case_context=case_context,
                )
                detail["mode"] = self.deps.model_provider.name
                detail["prompt_version"] = self.deps.model_provider.prompt_version

            if policy.decision == Decision.REVIEW and policy.detected_action != ActionKind.READ:
                case_id = request.case_id or "UNSPECIFIED"
                fields = self._fields_for_action(policy.detected_action)
                proposed_action = self.deps.salesforce.propose_case_update(
                    case_id=case_id,
                    fields=fields,
                    rationale="Generated from a user request; execution is gated by human approval.",
                    kind=policy.detected_action,
                )
                approval_id = self.deps.approvals.create(proposed_action, trace_id=trace_id)
                answer += (
                    f" A proposed {policy.detected_action.value} action was created but not executed. "
                    f"Approval reference: {approval_id}."
                )
                detail["approval_id"] = approval_id

        with trace.stage("evaluation") as detail:
            metrics = evaluate_response(
                answer=answer,
                documents=documents,
                policy=policy,
                minimum_groundedness=self.deps.settings.minimum_groundedness,
            )
            evaluation = EvaluationSummary.model_validate(metrics)
            detail.update(metrics)

        response = AssistResponse(
            trace_id=trace_id,
            answer=answer,
            policy=policy,
            citations=citations,
            proposed_action=proposed_action,
            approval_id=approval_id,
            evaluation=evaluation,
            trace=trace.steps,
        )
        self.deps.audit_logger.append(
            "workflow.completed",
            {
                "trace_id": trace_id,
                "query": request.query,
                "case_id": request.case_id,
                "decision": policy.decision.value,
                "detected_action": policy.detected_action.value,
                "approval_id": approval_id,
                "document_ids": [document.document_id for document in documents],
                "evaluation": evaluation.model_dump(),
                "model_provider": self.deps.model_provider.name,
                "prompt_version": self.deps.model_provider.prompt_version,
                "latency_ms": sum(step.latency_ms for step in trace.steps),
            },
        )
        return response

    @staticmethod
    def _fields_for_action(action: ActionKind) -> dict[str, Any]:
        if action == ActionKind.CLOSE_CASE:
            return {"Status": "Closed"}
        if action == ActionKind.ESCALATE:
            return {"Priority": "High", "Status": "Escalated"}
        if action == ActionKind.CREATE_REFUND:
            return {"Refund_Requested__c": True}
        return {"Status": "In Progress"}
