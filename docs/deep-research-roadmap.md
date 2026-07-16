# Deep Research Roadmap: Enterprise AI Architecture Portfolio

**Research date:** 2026-07-15  
**Primary target roles:** Salesforce AI Forward-Deployed Engineer (Lead/Principal) and Federal/DoD AI Architect  
**Portfolio principle:** demonstrate verifiable delivery evidence, not a catalog of package names.

## Executive conclusion

The strongest portfolio is one coherent enterprise use case implemented through a stable domain contract, with each framework or cloud provider treated as an adapter. The portfolio should prove five things:

1. **Problem framing:** convert an ambiguous customer or mission problem into an explicit workflow, authority boundary, and measurable acceptance criteria.
2. **Hands-on delivery:** implement retrieval, tools, orchestration, approval, integration, evaluation, observability, and deployment.
3. **Production judgment:** show where deterministic software is preferable to an agent and where human approval is mandatory.
4. **Risk management:** provide threat models, pre-deployment tests, traceability, incident handling, and honest limitations.
5. **Executive communication:** make the architecture understandable in ten minutes without hiding technical depth.

The research does **not** support turning the repository into a framework zoo. The best current projects explain a small set of primitives, offer a fast start, include runnable examples, and make production concerns visible: durable execution, human-in-the-loop control, tracing, evaluation, security, and deployment.

## Research findings

### 1. A portfolio needs four review paths

The repository should serve four audiences without forcing each audience to read everything:

| Audience | Time budget | Evidence surface |
|---|---:|---|
| Recruiter / hiring manager | 5-10 minutes | README, architecture image, demo, verified results, role mapping |
| Engineer | 20-45 minutes | one-command environment, source layout, tests, API contract, failure handling |
| Principal architect | 30-60 minutes | ADRs, data flow, trust boundaries, state model, tradeoffs, scaling path |
| Security / governance reviewer | 30-60 minutes | system card, threat model, approval boundaries, eval report, incident process |

This structure is more persuasive than listing every possible model, cloud, and orchestration framework in one README.

### 2. Use a framework-neutral domain core

The core workflow should own:

- domain state and data contracts;
- authorization and approval rules;
- retrieval and evidence objects;
- tool interfaces;
- evaluation events;
- audit and trace schemas.

Framework adapters should translate this contract into LangGraph, OpenAI Agents SDK, Microsoft Agent Framework, Salesforce Agentforce SDK, or Google ADK. This allows a fair comparison of orchestration frameworks without rewriting the business problem or changing the benchmark.

### 3. Framework priority has changed

The research changes the original tool priority:

1. **Salesforce Agentforce SDK and Salesforce REST** - direct relevance to JR346211. The official SDK supports programmatic agent definitions, prompt templates with Salesforce field mappings, modular directory formats, Apex generation, deployment validation, and MCP integration.
2. **LangGraph** - best fit for explicit durable workflows, checkpointing, pause/resume, and human approval.
3. **OpenAI Agents SDK** - useful for a small-primitives implementation with agents, tools, handoffs, guardrails, tracing, MCP, and human-in-the-loop workflows.
4. **Microsoft Agent Framework** - now the direct successor to AutoGen and Semantic Kernel. It combines agent abstractions with session state, type safety, middleware, telemetry, graph workflows, checkpointing, and human-in-the-loop control.
5. **Google ADK** - valuable as a later portability example because it includes graph and multi-agent workflows, deployment, evaluation, observability, safety controls, MCP, A2A, and multiple model providers.
6. **CrewAI, AutoGen, and Semantic Kernel** - retain as comparison or migration examples only. They should not all be first-class runtimes in the first release.

### 4. Evaluation must cover behavior, not only response text

A credible agent evaluation system needs five metric families:

- **Deterministic workflow gates:** policy decision, requested-action routing, approval routing, schema validation, allowed-tool enforcement.
- **Retrieval and response quality:** context precision, context recall, faithfulness, groundedness, response relevance, citation precision and recall.
- **Agent behavior:** tool-call accuracy, tool-call F1, goal completion, trajectory conformance, unnecessary tool calls, handoff correctness.
- **Operational quality:** latency, token usage, cost, retries, provider failures, recovery time, timeout and circuit-breaker behavior.
- **Human and safety quality:** reviewer override rate, inter-rater agreement, unsafe action prevention, prompt injection, data exfiltration, excessive agency, and incident severity.

The checked-in deterministic benchmark should remain the release gate. LLM judges and external frameworks should be supplemental because they add cost, provider variance, and evaluator-model bias.

### 5. Governance should be an engineering artifact

NIST's Generative AI Profile emphasizes governance, content provenance, pre-deployment testing, and incident disclosure. The public portfolio should therefore contain:

- a system card;
- a data and provenance statement;
- a threat model;
- an authority-boundary matrix;
- a pre-deployment evaluation report;
- a human-review design;
- an incident-response process;
- a change and release history.

These files should document controls and limitations, not claim certification.

### 6. Public GitHub presentation is part of the product

The repository should be discoverable and immediately inspectable:

- profile README repository named `silasj1022/silasj1022`;
- this repository pinned to the profile;
- focused repository topics;
- social preview image;
- short demo recording or animated GIF;
- Codespaces/dev-container support;
- tagged releases with generated notes;
- CI and security status visible;
- `CITATION.cff`, changelog, license, contributing guide, and security policy;
- SBOM and build provenance for releases.

## Current-state assessment

### Strong foundations

- Synthetic enterprise case and knowledge data.
- Framework-neutral orchestrator.
- Deterministic policy gate and approval-controlled writes.
- Salesforce REST adapter with safe synthetic fallback.
- Golden-set and adversarial datasets.
- Hash-chained audit events and structured traces.
- FastAPI interface, browser demo, Docker, Kubernetes, GitHub Actions, and GitLab CI configurations.
- Honest technology matrix distinguishing implemented, optional, and planned capabilities.

### Immediate risks

1. **Published-tree integrity:** the remote repository currently exposes some root files, while several essential files have not been consistently retrievable. A repository-integrity gate is now required before any resume link is treated as verified.
2. **No observed CI evidence:** there is no confirmed workflow run associated with the current public commit. README performance claims should be tied to a green workflow and downloadable artifacts.
3. **Local lint ergonomics:** using Ruff's `exclude` replaced default exclusions and caused a local virtual environment to be scanned. This has been corrected to `extend-exclude`.
4. **Framework freshness:** AutoGen and Semantic Kernel should no longer be presented as equal first-priority Microsoft paths because Microsoft now identifies Agent Framework as their direct successor.
5. **Metric semantics:** the current `mean_retrieved_source_coverage_proxy` measures cited retrieved documents rather than support coverage for response claims. It should be split into citation precision and citation recall before being used as a headline quality claim.

## Prioritized delivery plan

### P0 - Make every public claim reproducible

**Exit criteria**

- All required files are present in GitHub.
- `python scripts/verify_repository.py` succeeds on a fresh checkout.
- CI is green on supported Python versions.
- Evaluation and red-team reports are uploaded as workflow artifacts.
- README claims match the generated reports.
- A clean clone can run `make install verify-repo lint typecheck test evaluate red-team`.

### P1 - Recruiter-ready one-click experience

**Deliverables**

- GitHub Codespaces/dev-container support.
- `make demo` or equivalent one-command startup.
- 90-second demo recording.
- architecture image with trust boundaries;
- ten-minute recruiter path;
- evidence index linking each claim to code, test, and result.

### P1 - Salesforce Agentforce vertical

**Deliverables**

- Trailhead Playground or Developer Edition configuration guide.
- least-privilege connected app and OAuth instructions;
- modular Agentforce agent definition;
- prompt template with Account, Case, and Knowledge field mappings;
- validation-only deployment path;
- approval-controlled Case update action;
- MCP integration example;
- integration test using synthetic fixtures and a separately gated live-org smoke test.

### P1 - Evaluation and observability expansion

**Deliverables**

- failure taxonomy;
- citation precision and recall;
- tool-call and trajectory metrics;
- provider comparison dataset;
- OpenTelemetry spans following GenAI semantic conventions;
- MLflow evaluation run and dashboard export;
- human-review feedback schema;
- cost, latency, retry, and recovery metrics.

### P1 - Security and governance evidence pack

**Deliverables**

- system card and authority-boundary table;
- NIST AI RMF / GenAI Profile crosswalk;
- OWASP LLM and agentic-threat crosswalk;
- pre-deployment test report;
- incident response playbook;
- data provenance and retention statement;
- secret-scanning, dependency-review, and SBOM workflow.

### P2 - Comparable framework implementations

Implement the same customer-operations scenario and shared evaluation corpus with:

- LangGraph;
- OpenAI Agents SDK;
- Microsoft Agent Framework;
- Salesforce Agentforce SDK;
- Google ADK as a later portability lane.

Publish a comparison based on architecture, durability, approval semantics, observability, provider portability, code size, testability, latency, and operational burden. Do not rank frameworks with a single universal score.

### P2 - Production delivery and cloud variants

- immutable container image;
- non-root runtime and health checks;
- Kubernetes manifests and policy examples;
- Azure, AWS, and Google Cloud deployment guides;
- workload identity rather than long-lived keys;
- release SBOM and artifact attestation;
- load, fault-injection, and recovery tests.

### P3 - Public research and professional visibility

- publish a technical architecture paper;
- publish a benchmark methodology note;
- add a conference-style slide deck and recorded walkthrough;
- maintain `CITATION.cff` and tagged releases;
- create the GitHub profile README and pin the flagship work;
- publish sanitized case studies that distinguish implemented results from future work.

## Decision rules

- Add a framework only when it implements the shared scenario and passes the shared benchmark.
- Add a technology to the resume only after there is public code, a test, or a validated deployment artifact.
- Prefer deterministic code for fixed business rules and agent reasoning for ambiguity.
- Require attributable human approval for consequential writes.
- Never expose live customer, student, government, or employer data.
- Treat every benchmark as scoped evidence, not a production-scale claim.

## Primary sources

- Salesforce Agentforce SDK: https://github.com/salesforce/agent-sdk
- Salesforce REST API: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm
- Salesforce Well-Architected: https://architect.salesforce.com/well-architected/overview
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph interrupts: https://docs.langchain.com/oss/python/langgraph/interrupts
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- OpenAI evals: https://developers.openai.com/api/docs/guides/evals
- Microsoft Agent Framework: https://learn.microsoft.com/en-us/agent-framework/overview/
- Google ADK: https://adk.dev/
- MLflow GenAI evaluation: https://mlflow.org/docs/latest/genai/eval-monitor/
- Ragas metrics: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- OpenTelemetry GenAI conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1: https://doi.org/10.6028/NIST.AI.600-1
- OWASP GenAI Security Project: https://genai.owasp.org/
- GitHub profile README: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
- GitHub repository topics: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
