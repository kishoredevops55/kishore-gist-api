
import pytest
import httpx
import time

BASE_URL = "http://localhost:8080"

@pytest.fixture(scope="module")
def api_client():
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        yield client

def test_cache_behavior(api_client):
    """
    Simulate the demo_cache_testing.py logic:
    1. First request -> Miss (X-Cache: HIT should be missing or false, depends on implementation, usually we verify headers or timing)
       (Actually app/main.py doesn't seem to set X-Cache headers explicitly in the code I read, 
        let's re-read app/main.py if I missed it. If not, we infer from response time or side effects?)
    """
    # Just checking if we get data
    username = "octocat"
    
    # First call
    start = time.time()
    resp1 = api_client.get(f"/{username}")
    time1 = time.time() - start
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert "cache" in data1
    assert data1["cache"]["hit"] is False, "First request should not be cached"

    # Second call (should be cached)
    start = time.time()
    resp2 = api_client.get(f"/{username}")
    time2 = time.time() - start
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["cache"]["hit"] is True, "Second request should be cached"
    
    # We can also assert time2 < time1 significantly, but that's flaky in tests.

def test_pagination(api_client):
    """Test pagination works"""
    username = "octocat"
    resp = api_client.get(f"/{username}?per_page=1&page=1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["data"]) == 1
    assert data["pagination"]["per_page"] == 1
    assert data["pagination"]["page"] == 1

def test_unknown_user(api_client):
    """Test behavior for unknown user"""
    # Use a very random username
    resp = api_client.get(f"/thisuserdoesnotexist123456789xyz")
    # GitHub returns 404 for unknown user
    assert resp.status_code == 404
