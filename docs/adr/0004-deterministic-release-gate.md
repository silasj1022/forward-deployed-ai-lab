# ADR-0004: Deterministic release gate before optional LLM judges

- **Status:** Accepted
- **Date:** 2026-07-15

## Context

LLM-as-judge evaluation can add semantic depth but also introduces cost, provider availability, model drift, and judge variability. A continuous-integration gate must remain reproducible.

## Decision

Use versioned synthetic golden sets and deterministic checks for policy routing, action routing, approval routing, retrieval hits, citation coverage, groundedness proxy, and adversarial controls. Add RAGAS, DeepEval, garak, and MLflow as optional layers for credentialed evaluation and experiment tracking.

## Consequences

- Pull requests receive stable pass/fail signals without external APIs.
- Optional evaluators can enrich—not replace—the baseline evidence.
- The deterministic metrics are proxies and must not be presented as production model-quality measurements.
