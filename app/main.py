"""
GitHub Gists API
Simple FastAPI app to fetch public GitHub gists for any user.

Features:
- Fetch public gists for any GitHub user
- Pagination support (page, per_page parameters)
- In-memory caching with TTL (5 minutes default)
- Prometheus metrics for observability
- GitHub token support for higher rate limits
"""
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import logging
import os
import time
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TIMEOUT = 10.0
CACHE_TTL = int(os.environ.get("CACHE_TTL", 300))  # 5 minutes default


# ============================================================================
# In-Memory Cache Implementation
# ============================================================================
@dataclass
class CacheEntry:
    """Cache entry with data and expiration time."""
    data: Any
    expires_at: float


class SimpleCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if exists and not expired."""
        entry = self._cache.get(key)
        if entry is None:
            self._misses += 1
            return None
        
        if time.time() > entry.expires_at:
            del self._cache[key]
            self._misses += 1
            return None
        
        self._hits += 1
        return entry.data
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        expires_at = time.time() + (ttl or self._default_ttl)
        self._cache[key] = CacheEntry(data=value, expires_at=expires_at)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count of removed items."""
        now = time.time()
        expired_keys = [k for k, v in self._cache.items() if now > v.expires_at]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Return cache statistics."""
        return {
            "size": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self._hits / (self._hits + self._misses) if (self._hits + self._misses) > 0 else 0,
        }


# Global cache instance
gists_cache = SimpleCache(default_ttl=CACHE_TTL)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
)
ACTIVE_REQUESTS = Gauge(
    "http_requests_active",
    "Currently active HTTP requests",
)
GITHUB_API_REQUESTS = Counter(
    "github_api_requests_total",
    "Total GitHub API requests",
    ["status"],
)
CACHE_HITS = Counter(
    "cache_hits_total",
    "Total cache hits",
)
CACHE_MISSES = Counter(
    "cache_misses_total",
    "Total cache misses",
)


class GistInfo(BaseModel):
    """Gist data model"""

    id: str
    description: str | None
    url: str
    created_at: str
    files: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    service: str


class PaginatedResponse(BaseModel):
    """Paginated response with metadata"""
    
    data: List[GistInfo]
    pagination: Dict[str, Any]
    cache: Dict[str, Any]


class CacheStatsResponse(BaseModel):
    """Cache statistics response"""
    
    size: int
    hits: int
    misses: int
    hit_rate: float
    ttl_seconds: int


# Shared HTTP client
http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize HTTP client on startup and close on shutdown."""

    global http_client
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        logger.info("GitHub token configured - 5000 requests/hour")
    else:
        logger.warning("No GITHUB_TOKEN - limited to 60 requests/hour")
    
    http_client = httpx.AsyncClient(
        timeout=TIMEOUT,
        follow_redirects=True,
        headers=headers,
    )
    logger.info("App started")
    try:
        yield
    finally:
        if http_client:
            await http_client.aclose()
        logger.info("App stopped")

app = FastAPI(
    title="GitHub Gists API",
    description="Fetch public gists for any GitHub user",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware to allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to track request metrics."""

    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = time.time() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        return response
    finally:
        ACTIVE_REQUESTS.dec()


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""

    return PlainTextResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""

    return HealthResponse(status="healthy", service="github-gists-api")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint."""

    return HealthResponse(status="healthy", service="github-gists-api")


@app.get("/cache/stats", response_model=CacheStatsResponse)
async def cache_stats():
    """Get cache statistics."""
    stats = gists_cache.stats
    return CacheStatsResponse(
        size=stats["size"],
        hits=stats["hits"],
        misses=stats["misses"],
        hit_rate=stats["hit_rate"],
        ttl_seconds=CACHE_TTL,
    )


@app.delete("/cache")
async def clear_cache():
    """Clear the cache."""
    gists_cache.clear()
    logger.info("Cache cleared")
    return {"message": "Cache cleared successfully"}


@app.get("/{username}", response_model=PaginatedResponse)
async def get_user_gists(
    username: str = Path(..., description="GitHub username", min_length=1, max_length=39),
    page: int = Query(1, ge=1, le=100, description="Page number (1-100)"),
    per_page: int = Query(30, ge=1, le=100, description="Items per page (1-100)"),
    use_cache: bool = Query(True, description="Use cached data if available"),
) -> PaginatedResponse:
    """
    Fetch public gists for a GitHub user.
    
    Features:
    - **Pagination**: Use `page` and `per_page` to control results
    - **Caching**: Results are cached for 5 minutes (configurable via CACHE_TTL env var)
    - **Cache bypass**: Set `use_cache=false` to fetch fresh data
    
    Examples:
    - `GET /octocat` - Get first 30 gists (default)
    - `GET /octocat?page=2&per_page=10` - Get gists 11-20
    - `GET /octocat?use_cache=false` - Force fresh fetch from GitHub
    """

    if not http_client:
        raise HTTPException(status_code=500, detail="Service not ready")

    # Generate cache key
    cache_key = f"gists:{username}:page{page}:per_page{per_page}"
    cache_hit = False
    
    # Check cache first
    if use_cache:
        cached_data = gists_cache.get(cache_key)
        if cached_data is not None:
            logger.info("Cache hit for %s (page %d)", username, page)
            CACHE_HITS.inc()
            cache_hit = True
            return PaginatedResponse(
                data=cached_data["gists"],
                pagination=cached_data["pagination"],
                cache={"hit": True, "ttl_seconds": CACHE_TTL},
            )
    
    CACHE_MISSES.inc()
    
    # Build URL with pagination parameters
    url = f"{GITHUB_API_URL}/users/{username}/gists"
    params = {"page": page, "per_page": per_page}

    try:
        logger.info("Fetching gists for %s (page %d, per_page %d)", username, page, per_page)
        response = await http_client.get(url, params=params)

        GITHUB_API_REQUESTS.labels(status=response.status_code).inc()

        if response.status_code == 404:
            logger.warning("User not found: %s", username)
            raise HTTPException(status_code=404, detail=f"User '{username}' not found")

        if response.status_code == 403:
            logger.error("GitHub API rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="GitHub API rate limit exceeded. Please try again later.",
            )

        response.raise_for_status()
        gists_data = response.json()

        gists = [
            GistInfo(
                id=g["id"],
                description=g.get("description"),
                url=g["html_url"],
                created_at=g["created_at"],
                files=g["files"],
            )
            for g in gists_data
        ]

        # Parse Link header for pagination info
        link_header = response.headers.get("Link", "")
        has_next = 'rel="next"' in link_header
        has_prev = 'rel="prev"' in link_header
        
        pagination_info = {
            "page": page,
            "per_page": per_page,
            "count": len(gists),
            "has_next": has_next,
            "has_prev": has_prev,
        }

        # Cache the result
        gists_cache.set(cache_key, {"gists": gists, "pagination": pagination_info})

        logger.info("Found %d gists for %s (page %d)", len(gists), username, page)
        
        return PaginatedResponse(
            data=gists,
            pagination=pagination_info,
            cache={"hit": False, "ttl_seconds": CACHE_TTL},
        )

    except HTTPException:
        raise
    except httpx.TimeoutException:
        logger.error("Timeout fetching gists for %s", username)
        raise HTTPException(status_code=504, detail="GitHub API timeout")
    except httpx.HTTPStatusError as exc:
        logger.error("HTTP error: %s", exc)
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub error: {exc.response.status_code}",
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""

    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
