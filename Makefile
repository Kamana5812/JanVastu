.PHONY: up down build logs backend-install frontend-install frontend-build test
up:
	docker compose up --build -d
down:
	docker compose down
build:
	docker compose build
logs:
	docker compose logs -f api
backend-install:
	python -m pip install -r backend/requirements.txt
frontend-install:
	cd frontend && npm ci
frontend-build:
	cd frontend && npm run build
test:
	cd backend && python -m pytest -q
