"""
GitHub Gists API
Simple FastAPI app to fetch public GitHub gists for any user
"""
import logging
import time
from typing import List, Dict, Any
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"
TIMEOUT = 10.0

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)
ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Currently active HTTP requests'
)
GITHUB_API_REQUESTS = Counter(
    'github_api_requests_total',
    'Total GitHub API requests',
    ['status']
)


class GistInfo(BaseModel):
    """Gist data model"""
    id: str
    description: str | None
    url: str
    created_at: str
    files: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check"""
    status: str
    service: str


# Shared HTTP client
http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize HTTP client on startup, close on shutdown"""
    gmiddleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to track request metrics"""
    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    finally:
        ACTIVE_REQUESTS.dec()


@app.lobal http_client
    http_client = httpx.AsyncClient(
        timeout=TIMEOUT,
        follow_redirects=True,
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    logger.metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return PlainTextResponse(
        content=generate_latest().decode('utf-8'),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/info("App started")
    yield
    if http_client:
        await http_client.aclose()
    logger.info("App stopped")


app = FastAPI(
    title="GitHub Gists API",
    desc# Track GitHub API calls
        GITHUB_API_REQUESTS.labels(status=response.status_code).inc()
        
        ription="Fetch public gists for any GitHub user",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(status="healthy", service="github-gists-api")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint"""
    return HealthResponse(status="healthy", service="github-gists-api")


@app.get("/{username}", response_model=List[GistInfo])
async def get_user_gists(
    username: str = Path(..., description="GitHub username", min_length=1, max_length=39)
) -> List[GistInfo]:
    """
    Fetch public gists for a GitHub user
    
    Returns list of gists or appropriate error
    """
    if not http_client:
        raise HTTPException(status_code=500, detail="Service not ready")
    
    url = f"{GITHUB_API_URL}/users/{username}/gists"
    
    try:
        logger.info(f"Fetching gists for: {username}")
        response = await http_client.get(url)
        
        if response.status_code == 404:
            logger.warning(f"User not found: {username}")
            raise HTTPException(status_code=404, detail=f"User '{username}' not found")
        
        if response.status_code == 403:
            logger.error("GitHub API rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="GitHub API rate limit exceeded. Please try again later."
            )
        
        response.raise_for_status()
        gists_data = response.json()
        
        # Convert to our model
        gists = [
            GistInfo(
                id=g["id"],
                description=g.get("description"),
                url=g["html_url"],
                created_at=g["created_at"],
                files=g["files"]
            )
            for g in gists_data
        ]
        
        logger.info(f"Found {len(gists)} gists for {username}")
        return gists
    
    except HTTPException:
        # Preserve explicit HTTP errors we intentionally raise above
        raise
    except httpx.TimeoutException:
        logger.error(f"Timeout fetching gists for {username}")
        raise HTTPException(status_code=504, detail="GitHub API timeout")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"GitHub error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal error")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
