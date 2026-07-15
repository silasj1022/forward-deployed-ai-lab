.PHONY: install test lint format typecheck evaluate red-team run docker-build docker-run clean

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

test:
	pytest --cov=forward_deployed_ai_lab --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src

evaluate:
	python scripts/evaluate.py

red-team:
	python scripts/red_team.py

run:
	python -m forward_deployed_ai_lab

docker-build:
	docker build -t forward-deployed-ai-lab:local .

docker-run:
	docker run --rm -p 3000:3000 forward-deployed-ai-lab:local

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov artifacts/*.json logs/*.jsonl
