"""Application composition root."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import __version__
from .agents.orchestrator import ForwardDeployedOrchestrator, WorkflowDependencies
from .api.routes import router
from .config import Settings, get_settings
from .container import ApplicationContainer
from .models.providers import build_model_provider
from .observability import AuditLogger
from .tools import ApprovalStore, KnowledgeBase, PolicyEngine, SalesforceClient


def build_container(settings: Settings | None = None) -> ApplicationContainer:
    settings = settings or get_settings()
    data_dir = Path(settings.data_dir)
    knowledge_base = KnowledgeBase.from_json(data_dir / "knowledge_base.json")
    policy_engine = PolicyEngine()
    approvals = ApprovalStore()
    salesforce = SalesforceClient(settings, data_dir / "salesforce_cases.json")
    model_provider = build_model_provider(settings)
    audit_logger = AuditLogger(Path(settings.audit_log_path))
    dependencies = WorkflowDependencies(
        settings=settings,
        knowledge_base=knowledge_base,
        policy_engine=policy_engine,
        approvals=approvals,
        salesforce=salesforce,
        model_provider=model_provider,
        audit_logger=audit_logger,
    )
    orchestrator = ForwardDeployedOrchestrator(dependencies)
    return ApplicationContainer(
        settings=settings,
        knowledge_base=knowledge_base,
        policy_engine=policy_engine,
        approvals=approvals,
        salesforce=salesforce,
        model_provider=model_provider,
        audit_logger=audit_logger,
        orchestrator=orchestrator,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    container = build_container(settings)
    app = FastAPI(
        title=container.settings.app_name,
        version=__version__,
        description=(
            "Synthetic enterprise agent workflow with RAG, policy controls, human approvals, "
            "Salesforce integration, evaluation, and auditability."
        ),
    )
    app.state.container = container
    app.include_router(router)

    web_dir = Path(__file__).resolve().parents[2] / "web"
    if web_dir.exists():
        app.mount("/static", StaticFiles(directory=web_dir), name="static")

        @app.get("/", include_in_schema=False)
        def index() -> FileResponse:
            return FileResponse(web_dir / "index.html")

    return app


app = create_app()
