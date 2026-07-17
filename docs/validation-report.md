# Validation Report

**Validation date:** 2026-07-16

**Project version:** 1.0.0rc1

**Candidate status:** local validation complete and the public release-candidate workflow suite passed on PR #5; subsequent commits must re-pass the same gates

**Default runtime:** deterministic grounded provider with synthetic enterprise data

## Local automated checks

| Check | Result |
|---|---|
| Repository integrity / evidence consistency | Passed: 25 required paths, package and citation branding, encoding scan, dataset hashes, version metadata, and expected reports verified |
| Ruff lint | Passed |
| mypy strict type check | Passed across 43 source files |
| pytest | 30 passed; one upstream TestClient deprecation warning |
| Measured branch coverage | 88.43%; required minimum is 80% |
| Golden-set release gate | 10/10 cases passed |
| Adversarial/red-team gate | 8/8 cases passed |
| Python wheel | Built; clean-installed outside the checkout; data, web, API, evaluation, and red-team smoke test passed |
| Python source distribution | Built; clean-installed outside the checkout; data, web, API, evaluation, and red-team smoke test passed |
| CycloneDX SBOM | Generated and parsed as CycloneDX 1.6 with 24 resolved components |
| Runtime dependency audit | `pip-audit`: no known vulnerabilities found |
| Docker image | Built as `enterprise-agent-foundry:rc1`; live health returned `ok`; synthetic Salesforce mode and browser root returned successfully |

## Salesforce and approval resilience added for this candidate

- live REST query and update success paths;
- authentication failure without unsafe retry;
- timeout retry and recovery;
- HTTP 429 retry handling;
- bounded retry exhaustion for transient 5xx responses;
- exact-action SHA256 binding at approval time;
- deterministic execution idempotency key;
- successful-result replay without a second write;
- conflicting reviewer decisions and action substitution rejected.

These controls are process-local reference behavior. Durable identity-backed approvals, cross-process transactional claims, downstream idempotency, and live Salesforce org evidence remain production extensions.

## Synthetic evaluation scope

The golden set validates safe read-only requests, approved-knowledge retrieval, policy decisions, requested-action routing, human-approval routing, groundedness and retrieved-source checks, and prompt-injection, credential-exfiltration, and destructive-action boundaries.

Current generated metrics:

- case count: 10;
- quality-gate pass rate: 1.0;
- policy-decision accuracy: 1.0;
- action-routing accuracy: 1.0;
- approval-routing accuracy: 1.0;
- retrieval hit rate: 1.0;
- mean groundedness proxy: 0.9913;
- mean retrieved-source coverage proxy: 0.7667;
- red-team case count: 8;
- red-team pass rate: 1.0.

The benchmark is synthetic and intentionally small. It demonstrates repeatable workflow validation, not production model quality, user adoption, throughput, enterprise scale, Salesforce platform tenure, or claim-level citation recall.

## Coverage exclusions

Optional or deployment-specific adapters are excluded from the core coverage gate when their dependencies are not installed: LangGraph deployment adapter, MLflow experiment adapter, PySpark ingestion example, Chroma and Qdrant vector adapters, and the command-line entry point. These components remain separately labeled and require dedicated validation in their target environments.

## Public release gate

The release-candidate workflow suite on PR #5 passed on 2026-07-16:

- Python 3.11, 3.12, and 3.13 CI;
- wheel and source-distribution clean-install jobs;
- container build and live health smoke test;
- CodeQL;
- dependency review and dependency audit;
- repository, evaluation, and red-team evidence checks.

Do not merge or tag v1.0 if any later release-candidate commit fails one of these gates. Keep the pull request in draft until the remaining public-presentation corrections are reviewed.

The tag-triggered workflow is configured to rebuild and smoke-test both distributions, generate a resolved CycloneDX SBOM and SHA256 checksums, attest provenance, and attach the bundle to a GitHub Release. That tag execution is intentionally pending.
