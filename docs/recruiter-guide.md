# Recruiter and Hiring-Manager Guide

## What this project is intended to prove

This repository is not a collection of screenshots or package names. A reviewer can run the workflow, inspect the source, reproduce the synthetic evaluation reports, and see where policy and named human approval prevent an enterprise write.

## Five-minute scan

1. Read the top of `README.md` and the architecture diagram.
2. Open `docs/evidence-index.md` to distinguish verified, implemented, and planned work.
3. Review `docs/case-study-salesforce.md` or `docs/case-study-vtg.md` for role alignment.
4. Review `docs/system-card.md` for intended use, authority boundaries, and limitations.

## Ten-to-thirty-minute technical review

1. Inspect `src/forward_deployed_ai_lab/agents/orchestrator.py` for end-to-end workflow ownership.
2. Inspect `tools/policy.py`, `tools/salesforce.py`, and `tools/approvals.py` for governance and integration.
3. Inspect `evaluation/benchmark.py`, `data/eval/golden_set.json`, and `data/red_team/prompts.json` for measurable gates.
4. Inspect `observability/audit.py` and `observability/tracing.py` for evidence and traceability.
5. Inspect `.github/workflows/`, `Dockerfile`, `.devcontainer/`, and `infra/kubernetes/` for delivery discipline.
6. Run the UI and submit the built-in safe read, approval-gated write, and prompt-injection scenarios.

## Principal-architect review

- `docs/architecture.md`
- `docs/adr/`
- `docs/framework-strategy.md`
- `docs/framework-comparison-scorecard.md`
- `docs/evaluation-strategy.md`
- `docs/deep-research-roadmap.md`
- `docs/threat-model.md`

## Interview discussion prompts

- Why keep the default runtime deterministic while providing LLM adapters?
- Where should policy checks happen relative to retrieval, generation, approval, and execution?
- How should a Salesforce Developer Edition integration separate read, proposal, approval, and execution?
- Which evaluation metrics should block a release, and which should alert?
- How should interrupted workflows and reviewer decisions be persisted and recovered?
- Which framework best fits durable workflow control, platform-native Salesforce delivery, provider portability, or Microsoft/Azure deployment—and why?
- How would the architecture change for classified, disconnected, or zero-trust environments?

## Honest limitations

- The benchmark is synthetic and small.
- The in-memory approval store is not production persistence.
- The default response provider is not an LLM.
- Vector, cloud, Spark, external evaluation, and additional framework packages are optional or planned.
- The live Salesforce REST path is credential-gated; a verified public Agentforce org deployment is not yet claimed.
- No compliance certification or production scale is claimed.
- Local validation is not a substitute for a green public CI and release artifact trail.
