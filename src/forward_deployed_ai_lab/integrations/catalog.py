"""Honest capability catalog: implemented, optional, or documented only."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any

INTEGRATIONS: tuple[dict[str, Any], ...] = (
    {"name": "Salesforce REST API", "module": "httpx", "status": "implemented"},
    {"name": "LangGraph", "module": "langgraph", "status": "implemented-optional"},
    {"name": "LangChain", "module": "langchain", "status": "adapter-ready"},
    {"name": "Semantic Kernel", "module": "semantic_kernel", "status": "adapter-ready"},
    {"name": "CrewAI", "module": "crewai", "status": "adapter-ready"},
    {"name": "AutoGen", "module": "autogen_agentchat", "status": "adapter-ready"},
    {"name": "MLflow", "module": "mlflow", "status": "implemented-optional"},
    {"name": "RAGAS", "module": "ragas", "status": "evaluation-extension"},
    {"name": "DeepEval", "module": "deepeval", "status": "evaluation-extension"},
    {"name": "PySpark", "module": "pyspark", "status": "implemented-optional"},
    {"name": "Databricks SDK", "module": "databricks.sdk", "status": "adapter-ready"},
    {"name": "TensorFlow", "module": "tensorflow", "status": "modeling-extension"},
    {"name": "PyTorch", "module": "torch", "status": "modeling-extension"},
    {"name": "Hugging Face Transformers", "module": "transformers", "status": "modeling-extension"},
    {"name": "Chroma", "module": "chromadb", "status": "implemented-optional"},
    {"name": "Qdrant", "module": "qdrant_client", "status": "implemented-optional"},
    {"name": "Azure AI ML", "module": "azure.ai.ml", "status": "cloud-extension"},
    {"name": "AWS SageMaker", "module": "sagemaker", "status": "cloud-extension"},
    {"name": "Google Vertex AI", "module": "google.cloud.aiplatform", "status": "cloud-extension"},
    {"name": "OpenTelemetry", "module": "opentelemetry", "status": "observability-extension"},
)


def integration_catalog() -> list[dict[str, Any]]:
    catalog: list[dict[str, Any]] = []
    for item in INTEGRATIONS:
        module = item["module"]
        try:
            installed = find_spec(module) is not None
        except (ModuleNotFoundError, ValueError):
            installed = False
        catalog.append({**item, "installed": installed})
    return catalog
