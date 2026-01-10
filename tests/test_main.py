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
    assert isinstance(data, list)
    assert len(data) > 0  # octocat has public gists
    
    # Verify structure of first gist
    gist = data[0]
    assert "id" in gist
    assert "description" in gist
    assert "url" in gist
    assert "created_at" in gist
    assert "files" in gist
    assert isinstance(gist["files"], dict)


def test_get_gists_valid_user(api_running):
    """Test with another valid GitHub user"""
    response = httpx.get(f"{BASE_URL}/torvalds", timeout=10.0)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


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
