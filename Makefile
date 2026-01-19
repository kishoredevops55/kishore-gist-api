# Makefile for GitHub Gists API

PYTHON := python
PIP := pip
DOCKER := docker
IMAGE_NAME := github-gists-api
CONTAINER_NAME := github-gists-api-test
PORT := 8080

.PHONY: all help install build run stop test-unit test-integration test-functional test-sanity test-all clean

help:
	@echo "Available targets:"
	@echo "  install          Install dependencies (dev and prod)"
	@echo "  build            Build Docker image"
	@echo "  run              Run the application container in background"
	@echo "  stop             Stop the running application container"
	@echo "  test-unit        Run unit tests (no server required)"
	@echo "  test-integration Run integration tests (requires server running on port 8080)"
	@echo "  test-functional  Run functional tests (requires server running on port 8080)"
	@echo "  test-sanity      Run sanity checks (requires server running on port 8080)"
	@echo "  test-all         Build image, start server, run ALL tests, stop server"
	@echo "  serve            Start the API and Dashboard servers locally (requires local env)"
	@echo "  clean            Remove cache artifacts"

serve:
	@echo "Starting local servers..."
	$(PYTHON) start_all_servers.py

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

build:
	$(DOCKER) build -t $(IMAGE_NAME) .

run:
	$(DOCKER) run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	-$(DOCKER) rm -f $(CONTAINER_NAME)

REPORTS_DIR := reports

test-unit:
	$(DOCKER) run --rm -v "$(CURDIR):/app" -w //app python:3.12-slim-bookworm bash -c "pip install -q -r requirements-dev.txt && pytest tests/unit -v --html=$(REPORTS_DIR)/unit-report.html --self-contained-html --junitxml=$(REPORTS_DIR)/unit-junit.xml"

test-integration:
	$(DOCKER) run --rm -v "$(CURDIR):/app" -w //app --network container:$(CONTAINER_NAME) python:3.12-slim-bookworm bash -c "pip install -q -r requirements-dev.txt && pytest tests/integration -v --html=$(REPORTS_DIR)/integration-report.html --self-contained-html --junitxml=$(REPORTS_DIR)/integration-junit.xml"

test-functional:
	$(DOCKER) run --rm -v "$(CURDIR):/app" -w //app --network container:$(CONTAINER_NAME) python:3.12-slim-bookworm bash -c "pip install -q -r requirements-dev.txt && pytest tests/functional -v --html=$(REPORTS_DIR)/functional-report.html --self-contained-html --junitxml=$(REPORTS_DIR)/functional-junit.xml"

test-sanity:
	$(DOCKER) run --rm -v "$(CURDIR):/app" -w //app --network container:$(CONTAINER_NAME) python:3.12-slim-bookworm bash -c "pip install -q -r requirements-dev.txt && pytest tests/sanity -v --html=$(REPORTS_DIR)/sanity-report.html --self-contained-html --junitxml=$(REPORTS_DIR)/sanity-junit.xml"

test-all: build
	@echo "Starting server for full test suite..."
	$(MAKE) stop
	$(DOCKER) run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)
	@echo "Waiting for server to start (10s)..."
	@# Sleep command compatibility might vary on Windows if not using Git Bash/WSL. 
	@# Using python for cross-platform sleep
	$(PYTHON) -c "import time; time.sleep(10)"
	@echo "Running Unit Tests..."
	$(MAKE) test-unit
	@echo "Running Sanity Tests..."
	$(MAKE) test-sanity
	@echo "Running Functional Tests..."
	$(MAKE) test-functional
	@echo "Running Integration Tests..."
	$(MAKE) test-integration
	@echo "Cleaning up..."
	$(MAKE) stop

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
