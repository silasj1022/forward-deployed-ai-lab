# ADR-0001: Framework-neutral core with optional agent runtimes

- **Status:** Accepted
- **Date:** 2026-07-15

## Context

Forward-deployed teams frequently inherit customer constraints around cloud, models, orchestration frameworks, security boundaries, and deployment targets. Binding business logic to one agent framework makes the proof of value harder to test and migrate.

## Decision

Keep request handling, retrieval, policy, approval, evaluation, Salesforce integration, and audit logic in ordinary typed Python. Provide LangGraph as an optional adapter and document Semantic Kernel, CrewAI, AutoGen, and OpenAI Agents SDK as alternative integration paths rather than importing all of them into the primary runtime.

## Consequences

- Core tests run without model credentials or heavy agent dependencies.
- Customer-specific orchestration can change without rewriting business controls.
- The repository demonstrates depth rather than a framework-name collection.
- Framework-native features require adapters and separate integration testing.
