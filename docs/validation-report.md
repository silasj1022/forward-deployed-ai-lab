# Validation Report

**Validation date:** 2026-07-15  
**Project version:** 0.4.0 research baseline  
**Default runtime:** deterministic grounded provider with synthetic enterprise data

## Automated checks

| Check | Result |
|---|---|
| Repository integrity / evidence consistency | Passed: 24 required paths, dataset hashes, version metadata, and expected reports verified |
| Ruff lint | Passed for the complete project tree with local environments excluded |
| mypy strict type check | Passed across 41 source files |
| pytest | 21 passed |
| Measured coverage | 87.03% |
| Golden-set release gate | 10/10 cases passed |
| Adversarial/red-team gate | 8/8 cases passed |
| Python source distribution | Built successfully |
| Python wheel | Built successfully |
| Workflow and configuration YAML parse | Passed |

## Golden-set scope

The golden set validates deterministic behavior across:

- safe read-only requests;
- approved-knowledge retrieval;
- policy decisions;
- requested-action routing;
- human-approval routing;
- groundedness and retrieved-source checks;
- prompt-injection, credential-exfiltration, and destructive-action boundaries.

The benchmark is synthetic and intentionally small. It demonstrates repeatable workflow validation, not production model quality, user adoption, throughput, enterprise scale, or Salesforce platform tenure.

## Current generated metrics

- Case count: 10
- Quality-gate pass rate: 1.0
- Policy decision accuracy: 1.0
- Action-routing accuracy: 1.0
- Approval-routing accuracy: 1.0
- Retrieval hit rate: 1.0
- Mean groundedness proxy: 0.9913
- Mean retrieved-source coverage proxy: 0.7667
- Red-team case count: 8
- Red-team pass rate: 1.0

The source-coverage metric is not claim-level citation recall. The evaluation roadmap explicitly separates future citation precision and citation recall.

## Coverage exclusions

Optional or deployment-specific adapters are excluded from the core coverage gate when their dependencies are not installed:

- LangGraph deployment adapter;
- MLflow experiment adapter;
- PySpark ingestion example;
- Chroma and Qdrant vector adapters;
- command-line entry point.

These components are labeled separately in the technology matrix and require dedicated integration tests in their deployment environments.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
make validate
make build
```

Equivalent commands:

```bash
python scripts/verify_repository.py
ruff check .
mypy src/forward_deployed_ai_lab
pytest --cov=forward_deployed_ai_lab --cov-report=term-missing
python scripts/evaluate.py
python scripts/red_team.py
python -m build
```

## Public-verification status

Local validation has passed. A tagged release should not be described as publicly verified until:

1. the complete tree is present on GitHub;
2. GitHub Actions completes successfully;
3. the evaluation, red-team, and coverage artifacts are attached to the workflow;
4. the container build is green;
5. the release distributions receive GitHub artifact provenance.

The current execution environment did not provide a Docker daemon, so the container itself was not locally built during this validation run.
