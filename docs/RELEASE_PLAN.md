# Enterprise Agent Foundry Release Plan

## v0.4.0 - Research-backed public foundation

Purpose: establish the product identity, evidence model, governance standards, framework strategy, and public release path.

Evidence delivered:

- complete source tree and synthetic datasets;
- repository verification;
- lint, type-check, tests, evaluation, and red-team gates;
- container build and public CI artifacts;
- security and contribution policies;
- research-backed roadmap.

## v1.0.0-rc.1 - Release-fidelity candidate

Purpose: prove that source, wheel, container, approval controls, Salesforce failure handling, and release artifacts are reproducible before a final tag.

Exit criteria:

- wheel and source distribution include runtime data and web assets;
- both distributions pass clean-install smoke tests outside the checkout;
- approval decisions bind to exact action hashes and successful writes cannot replay;
- Salesforce HTTP success, auth, timeout, rate-limit, and retry exhaustion paths are tested;
- container builds and passes a live health check;
- Ruff, strict mypy, coverage, evaluation, red-team, CodeQL, dependency review, and dependency audit are green;
- release workflow generates SHA256 checksums, a CycloneDX SBOM, provenance attestations, and GitHub Release assets.

## v1.0.0 - Recruiter-ready flagship

The final tag is allowed only after the release-candidate pull request and all required checks are green. Repository settings, a short demonstration, and profile presentation are tracked separately because they are GitHub account configuration rather than distributable source.

## v1.1 - Durable workflow and framework comparison

- durable LangGraph checkpointer;
- pause/resume and recovery tests;
- persistent identity-backed approval records;
- OpenAI Agents SDK comparison adapter;
- Microsoft Agent Framework comparison adapter;
- trajectory and tool-call evaluation.

## v1.2 - Data and MLOps

- PySpark and Databricks-compatible ingestion demonstration;
- schema and lineage contracts;
- MLflow evaluation and experiment tracking;
- synthetic large-data workload;
- model, retrieval, latency, and cost comparisons.

## v1.3 - Cloud deployment blueprints

- Azure deployment reference;
- AWS deployment reference;
- Google Cloud deployment reference;
- workload identity and secret-management patterns;
- network, scaling, resilience, and recovery guidance.

## v1.4 - Salesforce-native and interoperability evidence

- Agentforce SDK project;
- prompt templates with Salesforce field mappings;
- validation-first deployment workflow;
- MCP tool exposure;
- OpenTelemetry GenAI spans;
- manually gated Salesforce Developer Edition smoke test.

## Release discipline

A release may not claim a capability based only on dependency installation, design documentation, or an untested adapter. Every release claim must be supported by code, tests, generated evidence, or a clearly labeled architecture artifact.
