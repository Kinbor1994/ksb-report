.PHONY: install dev test test-cov lint format build clean

install:
	pip install -e ".[dev]"

dev:
	uvicorn ksb_report.api.app:app --reload --port 8000

test:
	python -m pytest -v

test-cov:
	python -m pytest --cov=src/ksb_report --cov-report=term-missing

lint:
	ruff check src tests
	ruff format --check src tests

format:
	ruff format src tests
	ruff check --fix src tests

build:
	python -m build

clean:
	if exist dist rmdir /s /q dist
	if exist build rmdir /s /q build
	if exist *.egg-info rmdir /s /q *.egg-info
	if exist .pytest_cache rmdir /s /q .pytest_cache
	if exist .mypy_cache rmdir /s /q .mypy_cache
	if exist .ruff_cache rmdir /s /q .ruff_cache

release:
	@echo "Usage: make release VERSION=0.2.0"
	@echo "Steps:"
	@echo "  1. Update version in pyproject.toml and __init__.py"
	@echo "  2. Update CHANGELOG.md"
	@echo "  3. git add -A && git commit -m 'chore: release v$(VERSION)'"
	@echo "  4. git tag v$(VERSION)"
	@echo "  5. git push origin main --tags"
