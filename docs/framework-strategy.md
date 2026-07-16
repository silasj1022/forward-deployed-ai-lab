# Agent Framework Strategy

## Objective

Demonstrate architectural judgment and portability without maintaining five unrelated applications.

## Stable domain contract

Every implementation must consume and emit the same concepts:

- `WorkflowRequest`
- `WorkflowState`
- `PolicyDecision`
- `RetrievedEvidence`
- `ProposedAction`
- `ApprovalRecord`
- `ToolExecution`
- `EvaluationEvent`
- `AuditEvent`

The shared contract owns the business behavior. Framework adapters own execution semantics only.

## Priority lanes

| Priority | Framework/platform | Why it belongs | Required proof |
|---:|---|---|---|
| 1 | Salesforce Agentforce SDK + REST | Direct match to the Salesforce role and enterprise system of record | modular agent definition, prompt template, field mapping, validation-only deployment, approval-controlled write |
| 2 | LangGraph | Durable state, checkpointing, interrupts, explicit workflow control | pause/resume test, persistent thread, idempotent approval path |
| 3 | OpenAI Agents SDK | Small primitives, tools, handoffs, guardrails, tracing, MCP | tool guardrails, traced run, handoff test, workflow eval |
| 4 | Microsoft Agent Framework | Current Microsoft successor to AutoGen and Semantic Kernel, enterprise workflow and telemetry features | graph workflow, middleware, HITL, OpenTelemetry trace |
| 5 | Google ADK | Cloud-portable production lane with graph workflows, evaluation, deployment, MCP and A2A | shared-scenario adapter and benchmark |
| Comparison only | CrewAI, AutoGen, Semantic Kernel | Requested by the VTG role or useful for migration discussion, but not core portfolio dependencies | one bounded comparison example or migration note |

## Guardrail against a framework zoo

A framework is not added because it is popular. It is added only when:

1. it implements the same customer-operations scenario;
2. it uses the shared synthetic data;
3. it honors the same authority boundary;
4. it passes the same deterministic tests;
5. it emits compatible traces;
6. its differences are documented in an ADR.

## Comparison dimensions

- workflow clarity;
- durability and recovery;
- human-in-the-loop semantics;
- tool safety controls;
- memory and state handling;
- provider portability;
- observability;
- evaluation integration;
- deployment model;
- code size and cognitive load;
- latency and cost;
- operational failure modes.

No framework will receive a universal "best" label. Recommendations will be use-case-specific.
