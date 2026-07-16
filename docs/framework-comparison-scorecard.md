# Agent Framework Comparison Scorecard

This is a decision framework, not a universal ranking. Each implementation must use the same customer-operations scenario, domain contract, authority boundary, synthetic data, and evaluation set.

| Criterion | Salesforce Agentforce | LangGraph | OpenAI Agents SDK | Microsoft Agent Framework | Google ADK |
|---|---|---|---|---|---|
| Direct fit for JR346211 | Highest | High | High | High | Moderate |
| Enterprise system-of-record context | Native Salesforce advantage | Connector-defined | Connector-defined | Connector-defined | Connector-defined |
| Durable state / recovery | Platform-dependent validation required | Strong explicit checkpointing | Sessions/HITL; adapter proof required | Strong workflow/checkpointing focus | Workflow/session proof required |
| Human-in-the-loop | Action and platform controls | Interrupt/pause-resume model | Built-in HITL mechanisms | Workflow HITL and checkpointing | Supported; adapter proof required |
| Tool guardrails | Platform action design | Application-defined | First-class guardrails | Middleware and application controls | Application/plugin controls |
| Tracing / observability | Salesforce platform tooling | LangSmith/OTel integration path | Built-in tracing | OpenTelemetry integration | Evaluation/observability tooling |
| MCP / interoperability | SDK MCP server | MCP integrations | MCP tools | MCP ecosystem integration | MCP and A2A |
| Provider portability | Salesforce platform model choices | High | Provider-agnostic SDK path | High | High |
| Public portfolio priority | 1 | 2 | 3 | 4 | 5 |

## Selection guidance

- Choose **Agentforce** when Salesforce data, actions, deployment, and customer workflow are central.
- Choose **LangGraph** when explicit durable state, recovery, and human interruption are the dominant concerns.
- Choose **OpenAI Agents SDK** when a compact tools/handoffs/guardrails/tracing implementation is valuable.
- Choose **Microsoft Agent Framework** when Microsoft/Azure integration, middleware, telemetry, and production workflow patterns dominate.
- Choose **Google ADK** as a later portability lane involving Google Cloud, A2A, or ADK deployment patterns.

A framework earns a portfolio implementation only after it passes the shared deterministic gate and emits comparable evidence.
