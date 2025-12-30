.PHONY: dev prod down logs test init-db seed-db clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev       - Start development environment (hot-reload)"
	@echo "  make prod      - Start production environment"
	@echo "  make down      - Stop all containers"
	@echo "  make logs      - View container logs"
	@echo "  make test      - Run test suite"
	@echo "  make init-db   - Initialize database schema"
	@echo "  make seed-db   - Seed database with sample data"
	@echo "  make clean     - Remove containers, volumes, and cache"

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

# Run tests
test:
	pytest tests/ -v

# Initialize database schema
init-db:
	docker compose -f compose/docker-compose.yml exec api python scripts/init_db.py

# Seed database
seed-db:
	docker compose -f compose/docker-compose.yml exec api python scripts/seed_db.py

# Clean up everything
clean:
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml down -v --remove-orphans
	docker compose -f compose/docker-compose.yml -f compose/docker-compose.prod.yml down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
