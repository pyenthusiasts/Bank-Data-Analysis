.PHONY: help install install-dev test test-cov lint format type-check clean docs run example docker-build docker-run setup pre-commit

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
MYPY := mypy
PACKAGE := src/bank_analysis
TESTS := tests
EXAMPLES := examples

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package and dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: ## Install package with development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev,jupyter]"
	$(PIP) install pre-commit
	pre-commit install

setup: install-dev ## Complete development setup (install + pre-commit)
	@echo "✓ Development environment setup complete!"
	@echo "Run 'make test' to verify installation"

test: ## Run tests
	$(PYTEST) $(TESTS) -v

test-cov: ## Run tests with coverage
	$(PYTEST) $(TESTS) --cov=$(PACKAGE) --cov-report=html --cov-report=term-missing -v
	@echo "Coverage report generated in htmlcov/index.html"

test-fast: ## Run tests without coverage (faster)
	$(PYTEST) $(TESTS) -v --no-cov

lint: ## Run linting checks
	$(FLAKE8) $(PACKAGE) $(TESTS) $(EXAMPLES) --max-line-length=100 --extend-ignore=E203,W503

format: ## Format code with black
	$(BLACK) $(PACKAGE) $(TESTS) $(EXAMPLES) --line-length=100

format-check: ## Check code formatting without modifying
	$(BLACK) $(PACKAGE) $(TESTS) $(EXAMPLES) --check --line-length=100

type-check: ## Run type checking with mypy
	$(MYPY) $(PACKAGE) --ignore-missing-imports

check: lint format-check type-check ## Run all code quality checks

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .tox .eggs *.egg-info 2>/dev/null || true
	@echo "✓ Cleanup complete"

clean-data: ## Clean up data files (use with caution!)
	@echo "⚠️  This will delete all data files. Press Ctrl+C to cancel, or Enter to continue..."
	@read -r
	rm -f data/raw/*.csv data/raw/*.parquet data/raw/*.json
	rm -f data/processed/*.csv data/processed/*.parquet data/processed/*.json
	@echo "✓ Data files cleaned"

clean-output: ## Clean up output files
	rm -f output/plots/*.png output/plots/*.pdf output/plots/*.svg
	rm -f output/reports/*.pdf output/reports/*.html
	@echo "✓ Output files cleaned"

clean-all: clean clean-output ## Clean everything (code + output)
	@echo "✓ Complete cleanup done"

docs: ## Build documentation
	@echo "Documentation is in markdown format in the docs/ directory"
	@echo "View online: https://github.com/pyenthusiasts/Bank-Data-Analysis/tree/main/docs"

run: ## Run analysis with default configuration
	bank-analysis --config config.yaml

run-example: ## Run basic example
	$(PYTHON) examples/basic_analysis.py

run-custom: ## Run custom analysis example
	$(PYTHON) examples/custom_analysis.py

jupyter: ## Start Jupyter notebook server
	jupyter notebook notebooks/

build: ## Build distribution packages
	$(PYTHON) -m build
	twine check dist/*

publish-test: build ## Publish to TestPyPI
	twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI (use with caution!)
	@echo "⚠️  This will publish to PyPI. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	twine upload dist/*

docker-build: ## Build Docker image
	docker build -t bank-analysis:latest .

docker-run: ## Run Docker container
	docker-compose up

docker-clean: ## Remove Docker containers and images
	docker-compose down
	docker rmi bank-analysis:latest 2>/dev/null || true

benchmark: ## Run performance benchmarks
	$(PYTHON) scripts/benchmark.py

version: ## Show package version
	@$(PYTHON) -c "from bank_analysis import __version__; print(__version__)"

info: ## Show package information
	@echo "Bank Data Analysis Package Information"
	@echo "========================================"
	@echo "Version: $$($(PYTHON) -c 'from bank_analysis import __version__; print(__version__)')"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Location: $$($(PYTHON) -c 'import bank_analysis; print(bank_analysis.__file__)')"

tree: ## Show project structure
	@tree -I '__pycache__|*.pyc|*.egg-info|.git|.pytest_cache|htmlcov|dist|build' -L 3 || \
	find . -not -path '*/\.*' -not -path '*/__pycache__/*' -not -path '*/htmlcov/*' -not -path '*/dist/*' -not -path '*/build/*' -type d | sed 's|[^/]*/|  |g'

deps-update: ## Update dependencies
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt

deps-tree: ## Show dependency tree
	pip install pipdeptree
	pipdeptree

security-check: ## Run security checks
	pip install bandit safety
	bandit -r $(PACKAGE)
	safety check

watch-test: ## Watch files and run tests on change
	pip install pytest-watch
	ptw -- $(TESTS) -v

init-project: ## Initialize new project (first time setup)
	@echo "Initializing Bank Data Analysis project..."
	mkdir -p data/raw data/processed output/plots output/reports logs
	touch data/raw/.gitkeep data/processed/.gitkeep output/plots/.gitkeep output/reports/.gitkeep logs/.gitkeep
	cp config.yaml.example config.yaml 2>/dev/null || echo "No example config found"
	@echo "✓ Project initialized"

# Development shortcuts
dev: install-dev ## Alias for install-dev
t: test ## Alias for test
tc: test-cov ## Alias for test-cov
l: lint ## Alias for lint
f: format ## Alias for format
c: clean ## Alias for clean
r: run ## Alias for run

# Show current status
status: ## Show git and project status
	@echo "Git Status:"
	@git status -s
	@echo "\nBranch:"
	@git branch --show-current
	@echo "\nLast commit:"
	@git log -1 --oneline
	@echo "\nPackage info:"
	@make info
