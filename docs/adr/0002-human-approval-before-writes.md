# ADR-0002: Human approval before consequential writes

- **Status:** Accepted
- **Date:** 2026-07-15

## Context

Closing a case, changing priority, escalating an incident, or proposing a refund changes an enterprise system of record. A model-generated request or tool call is not sufficient authority for that action.

## Decision

Split every consequential action into proposal, approval, and execution stages. The proposal records the target, fields, rationale, trace ID, and action type. Execution requires an explicit approval decision. Live Salesforce writes additionally require two disabled-by-default configuration flags.

## Consequences

- The public demo can show a complete workflow without autonomous writes.
- Approval decisions are attributable and auditable.
- Production deployments must replace the in-memory store with durable identity-backed approval records and action-hash binding.
