# Case Study: Agentic Customer Operations on Salesforce

## Customer problem

A support organization wants faster case resolution using enterprise knowledge and AI, but it cannot permit an autonomous system to expose restricted data or change the system of record without approval.

## Delivered workflow

1. Validate the request, role, case ID, and intended action.
2. Retrieve synthetic Salesforce Case context.
3. Search approved knowledge and attach source-level citations.
4. Detect prompt injection, secrets, destructive actions, and insufficient evidence.
5. Draft a grounded response.
6. Convert consequential requests into proposed Salesforce Case changes.
7. Pause for a named human decision.
8. Execute an approved synthetic or live REST update.
9. Evaluate and append a tamper-evident audit event.

## Forward-deployed behaviors demonstrated

- Customer-problem decomposition
- Rapid, runnable proof of value
- Enterprise integration and data-contract thinking
- Technical tradeoff explanation
- Guardrails and human approval
- Measurable evaluation and operational telemetry
- Production deployment path

## Extension to Agentforce and Data Cloud

A production Salesforce implementation could replace the framework-neutral orchestration with Agentforce actions, use Data Cloud/Data 360 for governed customer context, expose the policy and evaluation services through APIs, and preserve the same approval and audit boundaries. This repository does not claim those platform components are implemented until a Developer Edition integration is completed and tested.
