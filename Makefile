.DEFAULT_GOAL := help
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help install dev migrate revision test lint fmt typecheck check clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate

install: $(VENV)/bin/activate  ## Create the virtualenv and install dependencies
	@test -f .env || cp .env.example .env

dev: install migrate  ## Run the development server on http://127.0.0.1:8000
	$(VENV)/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

migrate: install  ## Apply database migrations
	$(VENV)/bin/alembic upgrade head

revision: install  ## Autogenerate a migration: make revision m="add x"
	$(VENV)/bin/alembic revision --autogenerate -m "$(m)"

test: install  ## Run the test suite
	$(VENV)/bin/pytest

lint: install  ## Lint with ruff
	$(VENV)/bin/ruff check app tests scripts
	$(VENV)/bin/ruff format --check app tests scripts

fmt: install  ## Format with ruff
	$(VENV)/bin/ruff format app tests scripts
	$(VENV)/bin/ruff check --fix app tests scripts

typecheck: install  ## Type-check app/ with mypy
	$(VENV)/bin/mypy

check: lint typecheck test  ## Everything CI runs

clean:  ## Remove caches and the virtualenv
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
