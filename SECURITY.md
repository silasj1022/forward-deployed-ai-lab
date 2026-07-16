# Security Policy

## Public reference boundary

Enterprise Agent Foundry is a public, synthetic-data reference implementation. Do not submit real customer, student, patient, government, employer, export-controlled, classified, proprietary, or regulated data to this repository or any public demo. Do not commit credentials, OAuth tokens, private keys, production endpoints, security findings from live systems, or internal architecture details.

## Reporting a vulnerability

Report suspected vulnerabilities privately through GitHub Security Advisories when available. Do not open a public issue containing exploit details, credentials, or reproducible attack instructions against a live system.

A useful report includes:

- affected version or commit
- synthetic reproduction steps
- expected and observed behavior
- potential impact
- suggested mitigation, when known

## Supported version

The latest default branch and the latest published release are the only supported public-demo versions.

## Security design principles

- Consequential actions require attributable human approval.
- Live integrations remain disabled by default.
- Writes require explicit feature flags in addition to approval.
- Secrets are redacted before audit persistence.
- Audit events are hash chained for tamper evidence.
- Retrieval operates against approved synthetic knowledge in the default runtime.
- Agent tools should be deny-by-default and least privilege.
- External calls require timeouts, bounded retries, and explicit error handling.

## Required production changes

Before using these patterns with real data, implement and validate:

- enterprise identity and workload identity
- durable, access-controlled approval storage
- centralized secret management and key rotation
- network segmentation and egress policy
- locked dependencies, SBOM, container scanning, and signed provenance
- centralized telemetry, retention, and incident response
- privacy, legal, records-management, and data-governance review
- penetration testing and adversarial evaluation
- environment-specific authorization such as RMF, ATO, FedRAMP, or organizational security approval
- disaster recovery, rollback, and continuity testing

This repository does not claim certification or authorization for any regulated environment.
