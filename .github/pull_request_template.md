## What changed

Describe the customer, engineering, governance, or documentation change.

## Why

Explain the problem, tradeoff, and expected user or operator impact.

## Validation

- [ ] `ruff check .`
- [ ] `mypy src/forward_deployed_ai_lab`
- [ ] `pytest --cov=forward_deployed_ai_lab --cov-report=term-missing`
- [ ] `python scripts/evaluate.py`
- [ ] `python scripts/red_team.py`
- [ ] Documentation and capability-status labels remain accurate

## Security and data review

- [ ] No secrets, customer data, student data, government data, or proprietary content added
- [ ] Consequential actions remain approval-gated
- [ ] New external calls have timeouts, error handling, and least-privilege configuration
