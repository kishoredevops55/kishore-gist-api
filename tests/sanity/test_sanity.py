
import pytest
import httpx
import time

BASE_URL = "http://localhost:8080"

@pytest.fixture(scope="module")
def api_client():
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        yield client

def test_sanity_health(api_client):
    """Basic sanity check to ensure service is up"""
    try:
        response = api_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    except httpx.ConnectError:
        pytest.fail("Service is not reachable at localhost:8080. Is it running?")

def test_metrics_endpoint(api_client):
    """Ensure metrics are being exposed"""
    response = api_client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
