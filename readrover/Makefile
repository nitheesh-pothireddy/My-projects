.PHONY: install dev test lint typecheck demo eval clean help

PYTHON ?= python3
UV ?= uv

help:  ## Show available make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install:  ## Install runtime + demo dependencies
	$(UV) pip install -e ".[demo]"

dev:  ## Install dev + eval + trace deps and pre-commit hooks
	$(UV) pip install -e ".[dev,demo,eval,trace]"
	pre-commit install

test:  ## Run unit tests with coverage
	pytest

lint:  ## Run ruff
	ruff check src tests
	ruff format --check src tests

typecheck:  ## Run mypy
	mypy src

demo:  ## Launch Streamlit demo
	streamlit run demo/streamlit_app.py

eval:  ## Run full eval suite (~10 min)
	$(PYTHON) evals/run_eval.py

ask:  ## Run a single question. Usage: make ask Q="your question"
	@readrover ask "$(Q)"

clean:  ## Remove caches and build artefacts
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov
	find . -name __pycache__ -type d -exec rm -rf {} +
