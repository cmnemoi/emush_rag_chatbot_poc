all: setup-env-variables setup-git-hooks install check test 

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

evaluate-rag:
	uv run python scripts/evaluate_rag.py

index-documents:
	uv run python scripts/index_documents.py

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

run-chatbot:
	uv run fastapi dev emush_rag_chatbot/api.py --reload --host 0.0.0.0 --port 8000 

semantic-release:
	uv run semantic-release version --no-changelog --no-push --no-vcs-release --skip-build --no-commit --no-tag
	uv lock
	git add pyproject.toml uv.lock
	git commit --allow-empty --amend --no-edit

setup-env-variables:
	cp .env.example .env

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	chmod +x hooks/post-commit
	git config core.hooksPath hooks

test:
	uv run pytest -v --cov=emush_rag_chatbot --cov-report=xml

.PHONY: all check check-format check-lint check-types install lint run-chatbot semantic-release setup-env-variables setup-git-hooks test