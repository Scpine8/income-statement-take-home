.DEFAULT_GOAL := help

BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: help install backend frontend test test-backend test-frontend lint format

help:
	@echo "Targets:"
	@echo "  make install        Install backend (uv) and frontend (bun) dependencies"
	@echo "  make backend        Run the API on http://localhost:8000"
	@echo "  make frontend       Run the Next.js app on http://localhost:3000"
	@echo "  make test           Run backend and frontend tests"
	@echo "  make test-backend   Run pytest"
	@echo "  make test-frontend  Run bun test"
	@echo "  make lint           Run Biome"
	@echo "  make format         Apply Biome fixes"
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

lint:
	$(FRONTEND_DIR)/node_modules/.bin/biome check .

format:
	$(FRONTEND_DIR)/node_modules/.bin/biome check --write .
