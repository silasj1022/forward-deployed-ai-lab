# System Card

## System name

Forward-Deployed AI Delivery Lab

## Purpose

A public, synthetic reference implementation for demonstrating enterprise AI delivery patterns: retrieval, policy controls, agent orchestration, Salesforce integration, human approval, evaluation, observability, and auditability.

## Intended users

- recruiters and hiring managers evaluating forward-deployed AI experience;
- engineers reviewing implementation patterns;
- architects reviewing tradeoffs and deployment extensions;
- governance reviewers assessing authority boundaries and test evidence.

## Intended uses

- read-only answers grounded in an approved synthetic knowledge base;
- synthetic Salesforce Case context retrieval;
- generation of proposed Case actions;
- attributable human approval before consequential writes;
- deterministic evaluation and adversarial testing;
- local demonstration and architecture discussion.

## Out-of-scope uses

- live customer support without additional validation;
- autonomous financial, personnel, legal, medical, or mission decisions;
- storage of real customer, student, government, or employer data;
- classified processing;
- claims of FedRAMP, DoD, SOC 2, NIST, or Salesforce certification;
- production use of the deterministic response provider as a general LLM substitute.

## Data

All checked-in records are synthetic. No live credentials are committed. Live integrations are disabled by default and require explicit environment controls.

## Authority boundaries

| Action | Default authority |
|---|---|
| Retrieve approved synthetic knowledge | automatic |
| Read synthetic Salesforce context | automatic |
| Draft a response or proposed action | automatic |
| Close, update, escalate, or refund a Case | named human approval required |
| Bulk delete, bypass policy, expose secrets, or alter audit history | blocked |

## Human oversight

Approval records must identify the reviewer and decision. Consequential actions are proposed before execution. The live connector independently checks write-enablement configuration so the orchestration layer is not the only control.

## Evaluation

The release baseline includes deterministic workflow tests, a versioned golden set, and an adversarial dataset. External LLM-judge and production-monitoring integrations are optional and must not replace deterministic safety gates.

## Known limitations

- synthetic data and small evaluation sets;
- deterministic response generation does not establish real-model quality;
- no verified public Salesforce org deployment yet;
- optional cloud, vector, MLflow, Spark, and framework adapters require separate validation;
- current citation coverage is a retrieved-document proxy, not claim-level citation recall;
- public CI evidence must be established before the repository is represented as release-verified.

## Incident handling

Security concerns should be reported through `SECURITY.md`. A production adaptation should add incident severity, containment, rollback, evidence preservation, notification, and post-incident review procedures.

## Change management

Changes are versioned in Git, evaluated against checked-in datasets, and should be released only after required CI, security, and evidence-integrity checks pass.
