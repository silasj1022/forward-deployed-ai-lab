# ADR-0002: Human approval before consequential writes

- **Status:** Accepted
- **Date:** 2026-07-15

## Context

Closing a case, changing priority, escalating an incident, or proposing a refund changes an enterprise system of record. A model-generated request or tool call is not sufficient authority for that action.

## Decision

Split every consequential action into proposal, approval, and execution stages. The proposal records the target, fields, rationale, trace ID, and action type. The approval stores a canonical SHA256 hash of that exact proposal. Execution requires an explicit matching approval decision, claims a deterministic idempotency key, and stores the outcome so a successful request cannot issue the write twice. Live Salesforce writes additionally require two disabled-by-default configuration flags.

## Consequences

- The public demo can show a complete workflow without autonomous writes.
- Approval decisions record a named reviewer and are auditable within the reference workflow.
- The reference implementation prevents same-process replay and action substitution.
- Production deployments must replace the in-memory store with durable identity-backed approval records, transactional execution claims, and a downstream idempotency contract.
