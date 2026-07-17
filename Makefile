.PHONY: install verify-repo lint format typecheck test evaluate red-team validate run demo docker-build docker-run build clean

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

verify-repo:
	python scripts/verify_repository.py

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src/forward_deployed_ai_lab

test:
	pytest --cov=forward_deployed_ai_lab --cov-report=term-missing

evaluate:
	python scripts/evaluate.py

red-team:
	python scripts/red_team.py

validate: verify-repo lint typecheck test evaluate red-team

run:
	python -m forward_deployed_ai_lab

demo: run

docker-build:
	docker build -t enterprise-agent-foundry:local .

docker-run:
	docker run --rm -p 3000:3000 enterprise-agent-foundry:local

build:
	python -m build

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov build dist *.egg-info logs/*.jsonl
