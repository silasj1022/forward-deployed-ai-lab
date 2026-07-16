from __future__ import annotations

import importlib.util
import json

PACKAGES = {
    "Agent orchestration": [
        "langgraph",
        "langchain",
        "semantic_kernel",
        "crewai",
        "autogen_agentchat",
    ],
    "Deep learning": ["torch", "tensorflow", "transformers"],
    "Evaluation and MLOps": ["ragas", "deepeval", "fairlearn", "shap", "mlflow"],
    "Data platform": ["pyspark", "databricks"],
    "Vector databases": ["chromadb", "qdrant_client", "weaviate", "faiss"],
    "Cloud": ["azure.ai.ml", "boto3", "sagemaker", "google.cloud.aiplatform"],
    "Observability": ["opentelemetry", "prometheus_client"],
}

report = {
    group: {name: importlib.util.find_spec(name) is not None for name in names}
    for group, names in PACKAGES.items()
}
print(json.dumps(report, indent=2))
