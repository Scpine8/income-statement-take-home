.DEFAULT_GOAL := help

BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: help install backend frontend test test-backend test-frontend lint lint-backend lint-frontend format format-backend format-frontend

help:
	@echo "Targets:"
	@echo "  make install        Install backend (uv) and frontend (bun) dependencies"
	@echo "  make backend        Run the API on http://localhost:8000"
	@echo "  make frontend       Run the Next.js app on http://localhost:3000"
	@echo "  make test           Run backend and frontend tests"
	@echo "  make test-backend   Run pytest"
	@echo "  make test-frontend  Run bun test"
	@echo "  make lint           Run backend (Ruff, Pyright) and frontend (Biome) linters"
	@echo "  make lint-backend   Run Ruff and Pyright"
	@echo "  make lint-frontend  Run Biome"
	@echo "  make format         Apply Ruff and Biome formatting / fixes"
	@echo "  make format-backend Apply Ruff fixes and formatting"
	@echo "  make format-frontend Apply Biome fixes"
	@echo ""
	@echo "Run 'make backend' and 'make frontend' in two terminals."

install:
	cd $(BACKEND_DIR) && uv sync
	cd $(FRONTEND_DIR) && bun install

backend:
	cd $(BACKEND_DIR) && uv run uvicorn app.main:app --reload --port 8000

frontend:
	cd $(FRONTEND_DIR) && bun run dev

test: test-backend test-frontend

test-backend:
	cd $(BACKEND_DIR) && uv run pytest

test-frontend:
	bun test

lint: lint-backend lint-frontend

lint-backend:
	cd $(BACKEND_DIR) && uv run ruff check .
	cd $(BACKEND_DIR) && uv run pyright

lint-frontend:
	$(FRONTEND_DIR)/node_modules/.bin/biome check .

format: format-backend format-frontend

format-backend:
	cd $(BACKEND_DIR) && uv run ruff format .
	cd $(BACKEND_DIR) && uv run ruff check --fix .

format-frontend:
	$(FRONTEND_DIR)/node_modules/.bin/biome check --write .
