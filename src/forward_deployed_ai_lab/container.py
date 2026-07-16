"""Typed application dependencies shared by composition and API layers."""

from __future__ import annotations

from dataclasses import dataclass

from .agents.orchestrator import ForwardDeployedOrchestrator
from .config import Settings
from .models.base import ModelProvider
from .observability import AuditLogger
from .tools import ApprovalStore, KnowledgeBase, PolicyEngine, SalesforceClient


@dataclass
class ApplicationContainer:
    """Runtime services assembled by the application composition root."""

    settings: Settings
    knowledge_base: KnowledgeBase
    policy_engine: PolicyEngine
    approvals: ApprovalStore
    salesforce: SalesforceClient
    model_provider: ModelProvider
    audit_logger: AuditLogger
    orchestrator: ForwardDeployedOrchestrator
