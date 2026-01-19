
import pytest
import time
from unittest.mock import patch, AsyncMock
from app.main import SimpleCache, app
from fastapi.testclient import TestClient

# ==========================================
# Unit Tests for SimpleCache
# ==========================================

def test_cache_set_get():
    cache = SimpleCache(default_ttl=60)
    cache.set("foo", "bar")
    assert cache.get("foo") == "bar"

def test_cache_expiration():
    cache = SimpleCache(default_ttl=60)
    
    with patch("time.time") as mock_time:
        # Start time
        mock_time.return_value = 1000.0
        cache.set("foo", "bar", ttl=10) # Expires at 1010
        
        # Advance time within TTL
        mock_time.return_value = 1005.0
        assert cache.get("foo") == "bar"
        
        # Advance time past TTL
        mock_time.return_value = 1011.0
        assert cache.get("foo") is None
        assert cache._misses == 1

def test_cache_cleanup():
    cache = SimpleCache(default_ttl=60)
    with patch("time.time") as mock_time:
        mock_time.return_value = 1000.0
        cache.set("k1", "v1", ttl=5)
        cache.set("k2", "v2", ttl=20)
        
        # Advance time to expire k1 but not k2
        mock_time.return_value = 1010.0
        removed = cache.cleanup_expired()
        
        assert removed == 1
        assert "k1" not in cache._cache
        assert "k2" in cache._cache

def test_cache_stats():
    cache = SimpleCache()
    cache.set("a", 1)
    cache.get("a") # hit
    cache.get("b") # miss
    
    stats = cache.stats
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["size"] == 1

# ==========================================
# Unit Tests for App Routes (using TestClient)
# ==========================================

client = TestClient(app)

def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Note: Testing /{username} requires mocking httpx.AsyncClient or respx.
# Since app.main.http_client is global, we need to mock it properly in the context of the running app or dependency.,
# For this basic unit test coverage, we've covered the components and basic routes.
