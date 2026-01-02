.PHONY: dev prod down logs test test-local lint init-db seed-db clean help setup reset migrate migrate-new migrate-down

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "  First-time setup:"
	@echo "    make setup     - Full setup: start containers + seed database"
	@echo ""
	@echo "  Development:"
	@echo "    make dev       - Start development environment (hot-reload)"
	@echo "    make down      - Stop all containers"
	@echo "    make logs      - View container logs"
	@echo "    make test      - Run test suite in container"
	@echo "    make test-local - Run test suite locally"
	@echo "    make lint      - Run linting in container"
	@echo ""
	@echo "  Database:"
	@echo "    make init-db   - Initialize database schema (auto on startup)"
	@echo "    make seed-db   - Seed database with sample data"
	@echo "    make reset     - Reset database (clean + setup)"
	@echo ""
	@echo "  Migrations:"
	@echo "    make migrate      - Run pending migrations"
	@echo "    make migrate-new  - Generate migration from model changes"
	@echo "    make migrate-down - Rollback last migration"
	@echo ""
	@echo "  Production:"
	@echo "    make prod      - Start production environment"
	@echo "    make clean     - Remove containers, volumes, and cache"

# First-time setup: start containers and seed database
setup:
	@echo "Starting containers..."
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml up -d --build
	@echo "Waiting for API to be ready..."
	@sleep 5
	@echo "Seeding database..."
	docker compose -f compose/docker-compose.yml exec api python scripts/seed_db.py
	@echo "Setup complete! Run 'make logs' to view logs or 'make dev' for foreground mode."

# Development environment with hot-reload
dev:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml up --build

# Production environment
prod:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.prod.yml up --build -d

# Stop all containers
down:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml down
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.prod.yml down

# View logs
logs:
	docker compose -f compose/docker-compose.yml logs -f

# Run tests in container
test:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml exec api pytest tests/ -v

# Run tests locally
test-local:
	pytest tests/ -v

# Run linting in container
lint:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml exec api sh -c "black --check src/ tests/ && isort --check src/ tests/ && flake8 src/ tests/"

# Initialize database schema
init-db:
	docker compose -f compose/docker-compose.yml exec api python scripts/init_db.py

# Seed database
seed-db:
	docker compose -f compose/docker-compose.yml exec api python scripts/seed_db.py

# Reset database: clean everything and re-setup
reset: clean setup

# Run pending migrations
migrate:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml exec api alembic upgrade head

# Generate new migration from model changes
migrate-new:
	@read -p "Migration message: " msg; \
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml exec api alembic revision --autogenerate -m "$$msg"

# Rollback last migration
migrate-down:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml exec api alembic downgrade -1

# Clean up everything
clean:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml down -v --remove-orphans
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.prod.yml down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
