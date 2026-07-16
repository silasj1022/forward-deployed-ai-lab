# Contributing to Enterprise Agent Foundry

## Contribution principles

1. Do not add proprietary, employer, customer, government, student, patient, export-controlled, classified, or regulated data.
2. Keep the default workflow reproducible without paid model credentials.
3. Label every capability honestly as **implemented**, **implemented optional**, **planned**, or **architecture guidance**.
4. Preserve the framework-neutral domain contract, authority boundaries, synthetic scenario, evaluation schema, and audit model.
5. Keep consequential actions approval-gated, attributable, idempotent, and auditable.
6. Add tests and update the golden set for behavior changes.
7. Document architectural tradeoffs through an ADR when a change affects trust boundaries, orchestration, evaluation, storage, or deployment.

## Required validation

Run before opening a pull request:

```bash
make verify-repo
make lint
make typecheck
make test
make evaluate
make red-team
```

Changes involving containers, infrastructure, or releases should also validate the relevant Docker, Kubernetes, SBOM, and provenance paths.

## Pull request expectations

A pull request should explain:

- the customer, mission, engineering, or governance problem
- the proposed approach and alternatives considered
- the impact on security, privacy, evaluation, operations, and cost
- the evidence proving the change works
- whether the capability is core, optional, planned, or documentation-only

## Framework additions

Do not add a framework solely to increase keyword coverage. A new framework adapter must reuse the shared scenario and benchmark so reviewers can compare architecture, reliability, authority control, observability, and operational complexity.

## Public-project boundary

This project is a public reference implementation. Never include live credentials, private endpoints, real Salesforce records, employer artifacts, or non-public implementation details.
