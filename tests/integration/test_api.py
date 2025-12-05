"""
Integration tests for the TummyAI App API
Tests the full API endpoints with FastAPI TestClient
"""

import pytest
from fastapi.testclient import TestClient
from api.service import app

client = TestClient(app)


class TestAPIEndpoints:
    """Integration tests for API endpoints"""

    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "TummyAI App" in data["message"]

    def test_root_returns_json(self):
        """Test that root returns JSON content type"""
        response = client.get("/")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_euclidean_distance_endpoint(self):
        """Test the euclidean_distance endpoint"""
        response = client.get("/euclidean_distance/?x=3&y=4")
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 3
        assert data["y"] == 4
        assert data["distance"] == 5.0

    def test_euclidean_distance_default_parameters(self):
        """Test euclidean_distance with default parameters"""
        response = client.get("/euclidean_distance/")
        assert response.status_code == 200
        data = response.json()
        assert "distance" in data

    def test_euclidean_distance_with_floats(self):
        """Test euclidean_distance with floating point numbers"""
        response = client.get("/euclidean_distance/?x=1.5&y=2.0")
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 1.5
        assert data["y"] == 2.0
        assert isinstance(data["distance"], float)

    def test_invalid_route_returns_404(self):
        """Test that invalid routes return 404"""
        response = client.get("/this-route-does-not-exist")
        assert response.status_code == 404

    def test_method_not_allowed(self):
        """Test that POST to GET-only endpoint returns 405"""
        response = client.post("/")
        assert response.status_code == 405


class TestCORS:
    """Tests for CORS configuration"""

    def test_cors_enabled(self):
        """Test that CORS headers are present"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_all_origins(self):
        """Test that CORS allows all origins"""
        response = client.get("/", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "*"


@pytest.mark.asyncio
async def test_api_health_check():
    """Test that the API is healthy and responding"""
    response = client.get("/")
    assert response.status_code == 200
    # API should respond quickly
    assert response.elapsed.total_seconds() < 1 if hasattr(response, "elapsed") else True
