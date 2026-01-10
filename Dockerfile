# Multi-stage Dockerfile - Production Best Practices
# Stage 1: Build stage with dependencies
FROM python:3.12-slim-bookworm AS builder

# Security: Create non-root user for build
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage - Minimal and secure
FROM python:3.12-slim-bookworm AS runtime

# Metadata labels
LABEL maintainer="Equal Experts DevOps Team" \
      description="GitHub Gists API - FastAPI Application" \
      version="1.0.0"

# Security: Update system packages to fix CVEs and create non-root user
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gnupg2 \
    libpam-runtime \
    && rm -rf /var/lib/apt/lists/* && \
    groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser app/ ./app/

# Security: Set proper permissions
RUN chmod -R 755 /app && \
    chmod -R 555 /app/app

# Environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Security: Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8080/health', timeout=5.0)" || exit 1

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1", "--log-level", "info"]
