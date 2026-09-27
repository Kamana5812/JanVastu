.PHONY: up down build logs sh test lint format backend-install frontend-install frontend-build db-shell

# Docker Compose commands
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

# Backend commands
backend-install:
	cd backend && poetry install

test:
	cd backend && poetry run pytest

lint:
	cd backend && poetry run ruff check .
	cd backend && poetry run mypy app

format:
	cd backend && poetry run black .
	cd backend && poetry run ruff check --fix .

# Frontend commands
frontend-install:
	cd frontend/policymaker-dashboard && npm install
	cd frontend/public-portal && npm install

frontend-build:
	cd frontend/policymaker-dashboard && npm run build
	cd frontend/public-portal && npm run build

# Database
db-shell:
	docker-compose exec postgres psql -U janvastu -d janvastu
