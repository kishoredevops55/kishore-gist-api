#!/bin/bash
# Run tests against running Docker container

set -euo pipefail

# Prevent Git Bash path mangling for docker args on Windows
export MSYS2_ARG_CONV_EXCL="*"

echo "Building production image..."
docker build -t github-gists-api .

echo ""
echo "Starting API server..."
docker rm -f test-gists-api >/dev/null 2>&1 || true
docker run -d --rm -p 8080:8080 --name test-gists-api github-gists-api

# Ensure cleanup happens even if tests fail
cleanup() {
  echo ""
  echo "Stopping API server..."
  docker stop test-gists-api >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait for server to be ready
echo "Waiting for server to start..."
sleep 4

echo ""
echo "Running tests..."
docker run --rm \
  --network container:test-gists-api \
  -v "$PWD:/app" \
  -w /app \
  python:3.12-slim-bookworm \
  bash -c "pip install -q pytest httpx pytest-cov && pytest -v tests/"
