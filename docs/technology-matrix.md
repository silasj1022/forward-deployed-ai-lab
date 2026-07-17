# Technology and Evidence Matrix

This matrix is the source of truth for technology claims. A package name in `pyproject.toml` is not evidence that a capability is implemented.

Status meanings:

- **Verified:** exercised by automated tests or a reproducible command.
- **Implemented:** a substantive runnable path exists, but may require optional packages or credentials.
- **Planned adapter:** the framework has a defined contract and acceptance criteria; substantive implementation is not yet complete.
- **Architecture extension:** documented production path; not claimed as runtime experience from this repository alone.

| Area | Technology | Status | Evidence path |
|---|---|---|---|
| Language | Python 3.11–3.13 | Verified | `src/`, `tests/`, CI matrix |
| Notebook | Jupyter | Implemented walkthrough | `notebooks/01_evaluation_walkthrough.ipynb` |
| API | FastAPI / Pydantic | Verified | `src/forward_deployed_ai_lab/api/`, `app.py`, API tests |
| Domain workflow | Framework-neutral typed orchestrator | Verified | `agents/orchestrator.py`, `agents/state.py`, orchestrator tests |
| Durable workflow | LangGraph | Implemented optional | `agents/langgraph_adapter.py`, `agents/langgraph_app.py` |
| Agent platform | Salesforce Agentforce SDK | Planned adapter | `docs/agentforce-integration-plan.md`, `salesforce` extra |
| Agent framework | OpenAI Agents SDK | Planned adapter | `docs/framework-strategy.md`, `agents` extra |
| Agent framework | Microsoft Agent Framework | Planned adapter | `docs/framework-strategy.md`, `agents` extra |
| Agent framework | Google ADK | Planned adapter | `docs/framework-strategy.md`, `agents` extra |
| Framework comparison | Semantic Kernel / CrewAI / AutoGen | Architecture comparison | `framework-comparison` extra |
| Retrieval | BM25 | Verified | `tools/knowledge.py`, retrieval tests |
| Retrieval | Chroma / Qdrant | Implemented optional interface | `tools/vector.py` |
| Retrieval | FAISS / sentence-transformers | Architecture extension | `vector` extra |
| Enterprise integration | Salesforce REST / SOQL | Implemented | `tools/salesforce.py`, Salesforce tests |
| Enterprise integration | Agentforce prompt templates / deployment | Planned adapter | `docs/agentforce-integration-plan.md` |
| Evaluation | Deterministic golden-set gate | Verified | `evaluation/benchmark.py`, `data/eval/`, report artifact |
| Evaluation | Adversarial red-team gate | Verified | `evaluation/red_team.py`, `data/red_team/`, report artifact |
| Evaluation | Ragas / DeepEval / garak | Architecture extension | `evaluation` extra, `docs/evaluation-strategy.md` |
| Evaluation operations | MLflow | Implemented optional | `evaluation/mlflow_adapter.py` |
| Traditional ML | scikit-learn / Fairlearn / SHAP / Evidently | Architecture extension | `evaluation` and `ml` extras |
| Deep learning / NLP | TensorFlow / PyTorch / Hugging Face | Architecture extension | `ml` extra |
| Distributed data | PySpark / Databricks / Delta | Implemented optional example | `pipelines/spark_ingestion.py` |
| Containers | Docker / Compose | Verified build | `Dockerfile`, `docker-compose.yml`, public GitHub Actions container job |
| Orchestration | Kubernetes | Deployment manifest | `infra/kubernetes/`; no live cluster claim |
| Reproducibility | Dev Container / Codespaces | Implemented config | `.devcontainer/devcontainer.json` |
| CI/CD | GitHub Actions / GitLab CI | GitHub verified; GitLab config only | `.github/workflows/`, `.gitlab-ci.yml`; public GitHub Actions runs |
| Supply chain | Dependency review / pip-audit | Implemented config | security workflows |
| Supply chain | Release provenance / SBOM / checksums | Release-candidate config | `.github/workflows/release.yml`; tag execution intentionally pending |
| Cloud AI | Azure AI / Azure ML / Foundry | Architecture extension | `infra/cloud/`, `cloud` extra |
| Cloud AI | AWS SageMaker / Bedrock | Architecture extension | `infra/cloud/`, `cloud` extra |
| Cloud AI | Google Vertex AI | Architecture extension | `infra/cloud/`, `cloud` extra |
| Observability | Structured stage trace | Verified | `observability/tracing.py` and tests |
| Observability | Hash-chained audit | Verified | `observability/audit.py` and tests |
| Observability | OpenTelemetry / Prometheus | Planned extension | `observability` extra, evaluation roadmap |
| Governance | System card / threat model / ADRs | Implemented documentation | `docs/system-card.md`, `docs/threat-model.md`, `docs/adr/` |
| Portfolio evidence | Claim-to-test mapping | Verified locally and in CI | `docs/evidence-index.md`, `scripts/verify_repository.py`, CI logs |

A recruiter or hiring manager should use this matrix and the evidence index rather than infer experience from dependency declarations.
