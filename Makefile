.PHONY: check

# Run before every commit: same checks as CI, plus auto-fixes for lint and formatting.
check:
	uv run ruff check --fix
	uv run ruff format
	uv run mypy
	uv run pytest
