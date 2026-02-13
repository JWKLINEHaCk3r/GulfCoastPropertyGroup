"""
Makefile for Real Estate AI Ecosystem

Usage:
  make help              Show this help message
  make setup            Setup development environment
  make install          Install dependencies
  make migrate          Run database migrations
  make serve            Start FastAPI server
  make test             Run tests
  make docker-build     Build Docker images
  make docker-up        Start Docker Compose stack
  make docker-down      Stop Docker Compose stack
  make clean            Clean up generated files
"""

.PHONY: help setup install migrate serve test docker-build docker-up docker-down clean

help:
	@echo "Real Estate AI Ecosystem - Make Commands"
	@echo "========================================"
	@echo "make setup         - Setup development environment"
	@echo "make install       - Install dependencies"
	@echo "make serve         - Start FastAPI server"
	@echo "make test          - Run tests"
	@echo "make docker-build  - Build Docker images"
	@echo "make docker-up     - Start Docker Compose"
	@echo "make docker-down   - Stop Docker Compose"
	@echo "make clean         - Clean up generated files"

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	cp .env.example .env
	@echo "✅ Setup complete! Edit .env with your API keys"

install:
	. venv/bin/activate && pip install -r backend/requirements.txt

serve:
	cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	. venv/bin/activate && cd backend && pytest tests/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "✅ Stack is running!"
	@echo "API: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"

docker-down:
	docker-compose down
	@echo "✅ Stack stopped"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "✅ Cleaned up"
