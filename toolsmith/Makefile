.PHONY: install dev data train eval eval-all push test lint clean help

PYTHON ?= python3
UV ?= uv
HF_REPO ?= <your-username>/toolsmith-qwen2.5-0.5b

help:  ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install:  ## Install runtime deps only (for inference)
	$(UV) pip install -e .

dev:  ## Install everything (train + dev + hub)
	$(UV) pip install -e ".[train,dev,hub]"

data:  ## Generate synthetic training data via Claude (~$1)
	$(PYTHON) -m toolsmith.data.generate --n-train 1600 --n-val 200 --n-test 200

train:  ## Local LoRA training
	$(PYTHON) -m toolsmith.train

eval:  ## Score the trained adapter against the held-out test set
	$(PYTHON) -m toolsmith.eval --adapter ./outputs/lora-adapter

eval-all:  ## Score base + LoRA + frontier reference (Claude)
	$(PYTHON) -m toolsmith.eval --compare base,lora,reference

push:  ## Upload adapter + model card to HuggingFace Hub
	huggingface-cli upload $(HF_REPO) ./outputs/lora-adapter

test:  ## Run unit tests
	pytest

lint:  ## Run ruff
	ruff check src tests
	ruff format --check src tests

clean:  ## Remove caches + outputs
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache .coverage outputs wandb
	find . -name __pycache__ -type d -exec rm -rf {} +
