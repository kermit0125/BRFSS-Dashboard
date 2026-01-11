# Makefile for BRFSS Dashboard
# Provides convenient commands for common tasks

.PHONY: help install clean test lint format run pipeline

help:
	@echo "BRFSS Dashboard - Available Commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make clean      - Clean temporary files"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make run        - Run dashboard"
	@echo "  make pipeline   - Run data cleaning pipeline"

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete

test:
	pytest tests/ -v

lint:
	flake8 src/ --max-line-length=100
	mypy src/ || true

format:
	black src/ scripts/
	isort src/ scripts/

run:
	python src/dashboard_app.py

pipeline:
	python scripts/run_pipeline.py

