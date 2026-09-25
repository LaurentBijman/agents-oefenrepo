PYTHON ?= python

.PHONY: install test lint format check-agents

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

# Controleert de YAML-frontmatter van alle .agent.md-, SKILL.md- en .instructions.md-bestanden.
check-agents:
	$(PYTHON) scripts/check_frontmatter.py
