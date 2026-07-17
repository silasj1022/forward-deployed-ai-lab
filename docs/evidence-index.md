# Evidence Index

This file maps portfolio claims to inspectable evidence. A package name alone is not evidence of implementation.

Status definitions:

- **Verified:** exercised by automated tests or a reproducible local command.
- **Implemented:** source exists and has a runnable path, but may require optional packages or credentials.
- **Planned:** architecture or dependency path exists; no completed public demonstration yet.

| Claim | Status | Code or artifact | Verification |
|---|---|---|---|
| Framework-neutral enterprise workflow | Verified | `src/forward_deployed_ai_lab/agents/orchestrator.py` | `tests/test_orchestrator.py` |
| Typed workflow state and domain schemas | Verified | `agents/state.py`, `models/domain.py` | orchestrator and API tests |
| Approved-knowledge retrieval | Verified | `tools/knowledge.py`, `data/knowledge_base.json` | `tests/test_retrieval.py` |
| Grounded deterministic response provider | Verified | `models/deterministic.py` | provider and evaluation tests |
| Prompt-injection and secret controls | Verified | `tools/policy.py` | `tests/test_policy.py`, red-team report |
| Human approval before consequential writes | Verified | `tools/approvals.py`, `agents/orchestrator.py` | orchestrator and Salesforce tests |
| Synthetic Salesforce system of record | Verified | `tools/salesforce.py`, `data/salesforce_cases.json` | `tests/test_salesforce.py` |
| Live Salesforce REST adapter | Implemented | `tools/salesforce.py` | credential-gated; no public-org validation claimed |
| Salesforce Agentforce SDK integration | Planned | `docs/agentforce-integration-plan.md` | requires Developer Edition or Trailhead Playground |
| Golden-set release gate | Verified | `evaluation/benchmark.py`, `data/eval/golden_set.json` | `artifacts/evaluation-report.json` |
| Adversarial release gate | Verified | `evaluation/red_team.py`, `data/red_team/prompts.json` | `artifacts/red-team-report.json` |
| 30 automated tests / 88.43% measured coverage | Verified locally and in public CI | `tests/`, coverage configuration | Python 3.11-3.13 jobs on PR #5 |
| Hash-chained audit events | Verified | `observability/audit.py` | `tests/test_audit.py` |
| Structured stage tracing | Verified | `observability/tracing.py` | orchestrator and audit tests |
| FastAPI / OpenAPI interface | Verified | `app.py`, `api/` | `tests/test_api.py` |
| Browser demonstration | Implemented | `web/` | `make run` |
| Repository integrity and evidence hashes | Verified | `scripts/verify_repository.py` | `make verify-repo`, public CI |
| Dev Container / Codespaces setup | Implemented config | `.devcontainer/devcontainer.json` | public Codespaces proof pending |
| LangGraph pause/resume adapter | Implemented optional | `agents/langgraph_adapter.py`, `agents/langgraph_app.py` | optional dependency; persistent-store proof is planned |
| OpenAI Agents SDK adapter | Planned | `docs/framework-strategy.md` | shared-scenario adapter required |
| Microsoft Agent Framework adapter | Planned | `docs/framework-strategy.md` | shared-scenario adapter required |
| Google ADK adapter | Planned | `docs/framework-strategy.md` | shared-scenario adapter required |
| BM25 versus vector retrieval benchmark | Planned | `tools/vector.py` | comparative dataset and report required |
| MLflow evaluation tracking | Implemented optional | `evaluation/mlflow_adapter.py` | optional service/package |
| OpenTelemetry GenAI traces | Planned | observability dependency group | semantic-convention trace proof required |
| PySpark/Databricks ingestion example | Implemented optional | `pipelines/spark_ingestion.py` | optional runtime; scale benchmark planned |
| Docker image | Verified build and health smoke test | `Dockerfile`, `docker-compose.yml` | public container job on PR #5 |
| Wheel and source distribution | Release-candidate verified locally and in public CI | `pyproject.toml`, `scripts/installed_package_smoke.py` | clean-install smoke tests for both artifact types on PR #5 |
| Release provenance, SBOM, checksums, assets | Release-candidate config | `.github/workflows/release.yml` | tag intentionally pending until all RC checks are green |
| Dependency review | Verified | `.github/workflows/dependency-review.yml` | public pull-request workflow |
| Kubernetes deployment | Implemented manifest | `infra/kubernetes/` | cluster deployment is not yet claimed |
| NIST/OWASP governance artifacts | Implemented documentation | threat model and system card | crosswalk expansion planned |

## Current reproducible evidence

At the v1.0 release-candidate baseline:

- 30 automated tests pass locally on Python 3.12 and in the public Python 3.11-3.13 matrix.
- Measured branch coverage is 88.43% under documented exclusions, above the enforced 80% minimum.
- 10/10 synthetic golden-set cases pass the deterministic release gate.
- 8/8 synthetic adversarial cases pass.
- Mean groundedness is 0.9913 on the included synthetic dataset.
- Mean retrieved-source coverage proxy is 0.7667 under the current metric definition; it is not claim-level citation recall.

These are workflow-validation results on synthetic data, not claims of production-scale model performance.
