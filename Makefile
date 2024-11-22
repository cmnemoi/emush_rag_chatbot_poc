all: setup-git-hooks install check test 

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

semantic-release:
	uv run semantic-release version --no-changelog --no-push --no-vcs-release --skip-build

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	git config core.hooksPath hooks

test:
	uv run pytest -v --cov=emush_rag_chatbot --cov-report=xml

.PHONY: all check check-format check-lint check-types install lint semantic-release setup-git-hooks test