# Research and Reference Basis

**Research baseline:** 2026-07-15

The portfolio strategy and implementation were shaped by current official documentation and maintained reference repositories. Social-media project templates were treated only as layout inspiration, not as authority for architecture, security, evaluation, or platform claims.

## Research method

The research prioritized:

1. official product documentation;
2. maintained first-party GitHub repositories and samples;
3. current risk and governance publications;
4. reproducible repository and software-supply-chain guidance;
5. direct alignment to the Salesforce AI Forward-Deployed Engineer and VTG/Navy AI Architect capability sets.

Claims that can change over time—framework positioning, action versions, SDK capabilities, evaluation interfaces, and governance updates—must be rechecked before a major release.

## Agent architecture and orchestration

### Salesforce Agentforce

The Salesforce Agentforce SDK provides Python interfaces for defining, managing, validating, and deploying agents and prompt templates. Its documented capabilities include Salesforce field mappings, modular agent definitions, generated Apex support, and an MCP server. This makes it the highest-priority platform-specific extension for the Salesforce role.

- https://github.com/salesforce/agent-sdk
- https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm

### LangGraph

LangGraph is a low-level framework for long-running, stateful agents. Its documented production concerns—durable execution, persistence, interrupts, memory, and human-in-the-loop control—map directly to the repository's approval-gated workflow.

- https://github.com/langchain-ai/langgraph
- https://docs.langchain.com/oss/python/langgraph/persistence
- https://docs.langchain.com/oss/python/langgraph/interrupts
- https://docs.langchain.com/oss/python/langgraph/application-structure

### OpenAI Agents SDK

The OpenAI Agents SDK uses a small set of primitives: agents, tools, handoffs/agents-as-tools, guardrails, sessions, human-in-the-loop workflows, and tracing. It is prioritized as a compact provider-aware implementation of the shared scenario.

- https://github.com/openai/openai-agents-python
- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/tracing/

### Microsoft Agent Framework

Microsoft Agent Framework is Microsoft's current production-focused agent and workflow framework for Python and .NET. Microsoft documents graph workflows, checkpointing, streaming, middleware, OpenTelemetry, provider flexibility, and human-in-the-loop control, and provides migration guidance from AutoGen and Semantic Kernel. It therefore replaces those two frameworks as the primary Microsoft implementation lane in this portfolio.

- https://github.com/microsoft/agent-framework
- https://learn.microsoft.com/agent-framework/

### Google Agent Development Kit

Google ADK is retained as a later portability lane because its official materials cover agent composition, graph and multi-agent workflows, evaluation, observability, safety, deployment, MCP, A2A, and multiple model providers.

- https://google.github.io/adk-docs/

### Comparative samples

The Azure Samples repository provides a useful first-party pattern for comparing several frameworks against consistent environment and provider setup, including Codespaces and Dev Containers. The portfolio adopts the comparison discipline but keeps one shared enterprise scenario and benchmark.

- https://github.com/Azure-Samples/python-ai-agent-frameworks-demos

## Evaluation and observability

### Deterministic release gates

The default gate remains credential-free and deterministic so behavior can be reproduced in CI. LLM judges are supplemental rather than replacements for schema, policy, approval, tool, and audit contract tests.

### Ragas

Ragas documents metrics for retrieval and agent behavior, including context precision/recall, faithfulness, tool-call accuracy/F1, and agent-goal accuracy. Those metrics shape the next evaluation milestone.

- https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/

### MLflow

MLflow provides evaluation datasets, scorers, traces, experiment comparisons, human feedback, and production monitoring. The repository uses an optional adapter today and plans a full comparison/evidence lane.

- https://mlflow.org/docs/latest/ml/tracking/
- https://mlflow.org/docs/latest/genai/eval-monitor/

### OpenAI evaluation guidance

OpenAI's evaluation guidance emphasizes that evals are required to build reliable applications and to measure behavior when models, prompts, or system components change.

- https://platform.openai.com/docs/guides/evals

### OpenTelemetry

OpenTelemetry's Generative AI semantic conventions inform the planned vendor-neutral trace schema for model, retrieval, tool, approval, and workflow stages.

- https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Application and delivery structure

- FastAPI's multi-file guidance supports separation of routers, dependencies, schemas, and application setup.
- Pydantic Settings validates configuration and environment inputs.
- Docker's Python guidance informs the multi-stage, non-root container pattern.
- GitHub Actions' maintained actions and Python guidance inform the CI matrix, dependency cache, artifacts, and provenance workflow.

Official references:

- https://fastapi.tiangolo.com/tutorial/bigger-applications/
- https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- https://docs.docker.com/guides/python/
- https://docs.github.com/actions/tutorials/build-and-test-code/python
- https://github.com/actions/checkout
- https://github.com/actions/setup-python
- https://github.com/actions/upload-artifact
- https://github.com/actions/dependency-review-action
- https://github.com/actions/attest

## Governance and security

### NIST

NIST AI RMF 1.0 and the Generative AI Profile provide the repository's governance vocabulary and risk-treatment structure. The GenAI Profile highlights governance, content provenance, pre-deployment testing, and incident disclosure, along with risks such as confabulation, privacy harm, harmful bias, information-integrity failures, and problematic human-AI configurations.

- https://www.nist.gov/itl/ai-risk-management-framework
- https://doi.org/10.6028/NIST.AI.600-1
- https://airc.nist.gov/airmf-resources/playbook/

### OWASP

OWASP's LLM and agentic security materials inform the red-team categories: prompt injection, sensitive-information disclosure, excessive agency, unsafe tool use, and audit or control bypass.

- https://genai.owasp.org/llm-top-10/
- https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/

The repository uses these publications as design inputs and crosswalks. It does not claim certification or conformance assessment.

## GitHub portfolio and supply-chain research

GitHub's official guidance informed the profile README, pinned repository strategy, focused topics, Codespaces/Dev Container path, releases, dependency graph, SBOM planning, and signed artifact provenance.

- https://docs.github.com/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
- https://docs.github.com/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/pinning-items-to-your-profile
- https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
- https://docs.github.com/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph
- https://docs.github.com/repositories/releasing-projects-on-github/about-releases
- https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds
