.PHONY: help install dev build test lint format typecheck clean docker-up docker-down docker-logs db-init db-migrate db-makemigrations

# Default target
help:
	@echo "Mogumogu - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install all dependencies"
	@echo "  make db-init       Initialize database"
	@echo ""
	@echo "Development:"
	@echo "  make dev           Start all dev servers"
	@echo "  make dev-frontend  Start frontend dev server"
	@echo "  make dev-backend   Start backend dev server"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     Start all services with docker-compose"
	@echo "  make docker-down   Stop all services"
	@echo "  make docker-logs   View docker logs"
	@echo "  make docker-build  Build docker images"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests"
	@echo "  make test-frontend Run frontend tests"
	@echo "  make test-backend  Run backend tests"
	@echo "  make test-e2e      Run E2E tests"
	@echo "  make test-watch    Run tests in watch mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run all linters"
	@echo "  make format        Format all code"
	@echo "  make typecheck     Run type checking"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate    Run database migrations"
	@echo "  make db-makemigrations Create new migration"
	@echo ""
	@echo "Build:"
	@echo "  make build         Build all packages"
	@echo "  make clean         Clean build artifacts"

# Setup
install:
	npm ci
	cd backend && pip install -r requirements-dev.txt

db-init:
	cd backend && python -c "from app.database import init_db; init_db()"

# Development
dev:
	npm run dev

dev-frontend:
	npm run dev:frontend

dev-backend:
	npm run dev:backend

# Docker
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-build:
	docker-compose build

# Testing
test:
	npm run test

test-frontend:
	npm run test:frontend

test-backend:
	npm run test:backend

test-e2e:
	npm run test:e2e

test-watch:
	npm run test:watch --workspace=frontend & npm run test:watch --workspace=backend

# Code Quality
lint:
	npm run lint

format:
	npm run format

typecheck:
	npm run typecheck

# Database
db-migrate:
	cd backend && alembic upgrade head

db-makemigrations:
	@read -p "Migration message: " msg; \
	cd backend && alembic revision --autogenerate -m "$$msg"

# Build
build:
	npm run build

clean:
	rm -rf node_modules
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__
	rm -rf backend/app/routers/__pycache__
	rm -rf backend/app/services/__pycache__
	rm -rf .pytest_cache
	rm -rf coverage
	rm -rf frontend/coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true