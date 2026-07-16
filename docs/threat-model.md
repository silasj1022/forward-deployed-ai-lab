# Threat Model

## Protected assets

- Enterprise customer and case data
- Salesforce access tokens and connected-app credentials
- System prompts, policies, and tool configurations
- Approval decisions and audit evidence
- Model-provider credentials and cost budgets
- Integrity of system-of-record writes

## Principal threats and controls

| Threat | Example | Current control | Production extension |
|---|---|---|---|
| Prompt injection | Retrieved text tells the model to ignore policy | deterministic injection patterns; retrieved content treated as data | model-assisted classifier, content provenance, sandboxed tools |
| Secret exfiltration | request asks for access token | block rules and redaction | DLP, secret manager, egress policy |
| Unauthorized write | model closes a case | proposal-only design plus human approval | SSO identity, RBAC, transaction signing |
| Approval bypass | attacker calls execution directly | execution requires an explicit approved flag; API separates decision | durable approval token bound to action hash and reviewer |
| Hallucination | unsupported operational advice | approved retrieval, citations, groundedness gate | LLM judge plus domain adjudication and abstention |
| Data poisoning | altered knowledge record | curated synthetic corpus and audit evidence | signed source manifests, ingestion validation, lineage |
| Audit tampering | edit prior event | SHA-256 hash chain | WORM storage, SIEM export, independent verification |
| Cost or retry loop | unbounded model/tool calls | deterministic runtime and bounded workflow | budgets, circuit breakers, timeouts, model routing |
| Supply-chain compromise | malicious dependency/action | lean core, optional extras, CI | lockfiles, SBOM, Dependabot, pin actions by SHA |

## Non-goals

This public repository does not process controlled unclassified information, classified data, real student records, healthcare data, financial transactions, or live customer production data.
