# ADR-0003: Synthetic public data and disabled live writes

- **Status:** Accepted
- **Date:** 2026-07-15

## Context

A public portfolio should prove architecture and engineering ability without exposing employer, customer, student, government, or regulated data.

## Decision

Ship only synthetic cases, accounts, knowledge articles, evaluation prompts, and red-team inputs. Default to a local system-of-record adapter and a deterministic response provider. Keep networked models and Salesforce access opt-in through environment variables.

## Consequences

- Anyone can reproduce the demo without credentials.
- Public benchmark results are explicitly limited to workflow validation.
- Production scale, authorization, and model-quality claims require separate evidence.
