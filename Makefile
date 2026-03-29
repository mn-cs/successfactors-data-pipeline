UV := uv
PYTHON := $(UV) run python

.DEFAULT_GOAL := help

.PHONY: help install run scrape lint format clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "; print "Available commands:\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install project dependencies from pyproject.toml and uv.lock
	$(UV) sync --frozen --extra dev

run: install ## Run the full data pipeline
	$(PYTHON) src/dataset.py

scrape: install ## Refresh the Wikipedia scrape files only
	$(PYTHON) src/scrapers/date_of_birth.py
	$(PYTHON) src/scrapers/university_degree.py

lint: install ## Check formatting and lint rules
	$(UV) run ruff format --check
	$(UV) run ruff check

format: install ## Apply formatting and autofixes
	$(UV) run ruff check --fix
	$(UV) run ruff format

clean: ## Remove Python cache files
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
