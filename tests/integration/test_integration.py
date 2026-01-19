"""
Tests for GitHub Gists API
"""
import pytest
import httpx

# Base URL for the running API
BASE_URL = "http://localhost:8080"


@pytest.fixture(scope="session")
def api_running():
    """Check if API is running, skip tests if not"""
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    pytest.skip("API server not running on localhost:8080")


def test_health_check(api_running):
    """Test health endpoint"""
    response = httpx.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "github-gists-api"


def test_root(api_running):
    """Test root endpoint"""
    response = httpx.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "github-gists-api"


def test_get_gists_octocat(api_running):
    """Test fetching gists for 'octocat' user (required by exercise)"""
    response = httpx.get(f"{BASE_URL}/octocat", timeout=10.0)
    assert response.status_code == 200
    
    data = response.json()
    # New paginated response format
    assert "data" in data
    assert "pagination" in data
    assert "cache" in data
    
    gists = data["data"]
    assert isinstance(gists, list)
    assert len(gists) > 0  # octocat has public gists
    
    # Verify structure of first gist
    gist = gists[0]
    assert "id" in gist
    assert "description" in gist
    assert "url" in gist
    assert "created_at" in gist
    assert "files" in gist
    assert isinstance(gist["files"], dict)
    
    # Verify pagination metadata
    pagination = data["pagination"]
    assert "page" in pagination
    assert "per_page" in pagination
    assert "count" in pagination
    assert "has_next" in pagination
    assert "has_prev" in pagination


def test_get_gists_valid_user(api_running):
    """Test with another valid GitHub user"""
    response = httpx.get(f"{BASE_URL}/torvalds", timeout=10.0)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


def test_get_gists_user_not_found(api_running):
    """Test with non-existent GitHub user"""
    response = httpx.get(f"{BASE_URL}/thisuserdoesnotexist999999", timeout=10.0)
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_invalid_username_too_long(api_running):
    """Test username validation - too long"""
    long_username = "a" * 40  # Max is 39
    response = httpx.get(f"{BASE_URL}/{long_username}")
    assert response.status_code == 422


def test_response_format(api_running):
    """Test response format is valid JSON"""
    response = httpx.get(f"{BASE_URL}/octocat", timeout=10.0)
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


# ============================================================================
# Pagination Tests
# ============================================================================
def test_pagination_default(api_running):
    """Test default pagination (page=1, per_page=30)"""
    response = httpx.get(f"{BASE_URL}/octocat", timeout=10.0)
    assert response.status_code == 200
    data = response.json()
    
    pagination = data["pagination"]
    assert pagination["page"] == 1
    assert pagination["per_page"] == 30


def test_pagination_custom_page_size(api_running):
    """Test custom page size"""
    response = httpx.get(f"{BASE_URL}/octocat?per_page=5", timeout=10.0)
    assert response.status_code == 200
    data = response.json()
    
    assert data["pagination"]["per_page"] == 5
    assert data["pagination"]["count"] <= 5


def test_pagination_second_page(api_running):
    """Test fetching second page"""
    response = httpx.get(f"{BASE_URL}/octocat?page=2&per_page=5", timeout=10.0)
    assert response.status_code == 200
    data = response.json()
    
    assert data["pagination"]["page"] == 2
    assert data["pagination"]["has_prev"] == True


def test_pagination_invalid_page(api_running):
    """Test invalid page number"""
    response = httpx.get(f"{BASE_URL}/octocat?page=0")
    assert response.status_code == 422  # Validation error


def test_pagination_invalid_per_page(api_running):
    """Test invalid per_page value"""
    response = httpx.get(f"{BASE_URL}/octocat?per_page=101")
    assert response.status_code == 422  # Validation error (max is 100)


# ============================================================================
# Caching Tests
# ============================================================================
def test_cache_stats(api_running):
    """Test cache stats endpoint"""
    response = httpx.get(f"{BASE_URL}/cache/stats")
    assert response.status_code == 200
    data = response.json()
    
    assert "size" in data
    assert "hits" in data
    assert "misses" in data
    assert "hit_rate" in data
    assert "ttl_seconds" in data


def test_cache_hit(api_running):
    """Test that second request hits cache"""
    # First request (cache miss)
    response1 = httpx.get(f"{BASE_URL}/octocat?per_page=3", timeout=10.0)
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["cache"]["hit"] == False
    
    # Second request (cache hit)
    response2 = httpx.get(f"{BASE_URL}/octocat?per_page=3", timeout=10.0)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["cache"]["hit"] == True


def test_cache_bypass(api_running):
    """Test cache bypass with use_cache=false"""
    # Make sure cache has data
    httpx.get(f"{BASE_URL}/octocat?per_page=2", timeout=10.0)
    
    # Request with cache bypass
    response = httpx.get(f"{BASE_URL}/octocat?per_page=2&use_cache=false", timeout=10.0)
    assert response.status_code == 200
    data = response.json()
    assert data["cache"]["hit"] == False


def test_cache_clear(api_running):
    """Test cache clear endpoint"""
    # Populate cache
    httpx.get(f"{BASE_URL}/octocat", timeout=10.0)
    
    # Clear cache
    response = httpx.delete(f"{BASE_URL}/cache")
    assert response.status_code == 200
    assert "cleared" in response.json()["message"].lower()
    
    # Verify cache is empty
    stats = httpx.get(f"{BASE_URL}/cache/stats").json()
    assert stats["size"] == 0
