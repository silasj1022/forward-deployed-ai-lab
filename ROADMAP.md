# Enterprise Agent Foundry Roadmap

This roadmap is evidence-gated. A capability is not represented as complete until code, tests, generated evidence, and public validation are available.

## P0 — Public repository integrity

**Objective:** make every public claim independently reproducible from a clean checkout.

- Publish the complete validated source tree, tests, datasets, documentation, and workflows.
- Pass repository verification on a clean clone.
- Establish green GitHub Actions runs for Python 3.11, 3.12, and 3.13.
- Build the container in CI.
- Upload evaluation, red-team, and coverage artifacts.
- Keep README metrics synchronized with generated reports.
- Publish a research-backed `v0.4.0` release after CI is green.

**Exit criterion:** `make install verify-repo lint typecheck test evaluate red-team` succeeds from a fresh clone and the public workflow artifacts are inspectable.

## P1 — Recruiter-ready flagship release

- Rename the GitHub repository slug to `enterprise-agent-foundry` after the rebrand PR is merged.
- Add a 90-second demo recording and static social-preview image.
- Add a one-command `make demo` path.
- Validate Dev Container and GitHub Codespaces setup.
- Add an architecture image showing data flows, trust boundaries, and approval points.
- Protect `main` with required pull requests, required checks, resolved conversations, and disabled force pushes.
- Create the `silasj1022/silasj1022` profile README and pin this repository first.
- Tag the first recruiter-ready release as `v1.0.0`.

## P1 — Salesforce Agentforce vertical

- Configure a Salesforce Developer Edition or Trailhead Playground with synthetic Accounts, Contacts, Cases, and Knowledge.
- Implement a modular Agentforce agent definition.
- Add prompt templates with Salesforce field mappings.
- Add validation-first deployment and rollback instructions.
- Add a bounded MCP server/tool example.
- Demonstrate an approval-controlled Case update in the synthetic org.
- Keep the live-org smoke test manually gated and excluded from default CI.

## P1 — Evaluation and observability

- Replace the retrieved-source coverage proxy with claim-level citation precision and recall.
- Add context precision, context recall, faithfulness, response relevance, and unsupported-claim counts.
- Add tool-call accuracy/F1, trajectory conformance, handoff correctness, and unnecessary-tool metrics.
- Add cost, token, latency, retry, timeout, recovery, and circuit-breaker metrics.
- Emit OpenTelemetry spans aligned with current GenAI semantic conventions.
- Add an MLflow evaluation run and exportable dashboard evidence.
- Add a human-review feedback schema and reviewer-agreement analysis.

## P1 — Security and governance evidence pack

- Expand the NIST AI RMF and Generative AI Profile crosswalk.
- Expand the OWASP LLM and agentic-threat crosswalk.
- Add a pre-deployment evaluation report and incident-response playbook.
- Add data provenance, retention, and deletion statements.
- Add dependency review, SBOM generation, and signed release provenance.
- Add failure-injection tests for timeouts, provider outages, malformed tool output, and approval-store failures.

## P2 — Comparable framework adapters

Implement the same customer-operations scenario, authority boundary, datasets, and benchmark through:

1. LangGraph with durable checkpointing and pause/resume tests.
2. OpenAI Agents SDK with tool guardrails, handoffs, tracing, and MCP.
3. Microsoft Agent Framework with middleware, checkpointing, OpenTelemetry, and HITL.
4. Google ADK with graph/multi-agent workflow, evaluation, deployment, MCP, and A2A.

CrewAI, AutoGen, and Semantic Kernel remain bounded comparison or migration lanes unless a specific role or customer use case justifies deeper investment.

## P2 — Data and cloud architecture demonstrations

- Compare BM25, dense-vector, and hybrid retrieval on a versioned benchmark.
- Validate PySpark/Databricks ingestion on a synthetic large-data workload.
- Add cloud deployment blueprints for Azure, AWS, and Google Cloud.
- Add load, reliability, model-cost, and recovery testing.
- Add provider routing with explicit quality, latency, and cost thresholds.

## P3 — Portfolio extraction and community evidence

New repositories will be extracted only after a component has independent users, tests, and a release cadence.

Potential extractions:

- `ai-evaluation-framework`
- `ai-reference-architectures`
- `federal-ai-patterns`
- `enterprise-rag-patterns`

Additional goals:

- Publish versioned architecture papers and benchmark reports.
- Add conference-style diagrams and reproducible notebooks.
- Contribute a bounded improvement or documentation fix to a relevant open-source project.
- Publish release-linked research summaries through GitHub Releases and `CITATION.cff`.
