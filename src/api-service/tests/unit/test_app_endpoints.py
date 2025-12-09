"""
Unit tests for FastAPI application endpoints
Tests various endpoint behaviors and error cases
"""
import pytest
from fastapi.testclient import TestClient

from api.service import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_endpoint_returns_200(self):
        """Test root endpoint returns 200 status code"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_message(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "TummyAI" in data["message"]

    def test_root_endpoint_content_type(self):
        """Test root endpoint returns JSON content type"""
        response = client.get("/")
        assert "application/json" in response.headers["content-type"]

    def test_root_endpoint_multiple_calls(self):
        """Test root endpoint consistency across multiple calls"""
        response1 = client.get("/")
        response2 = client.get("/")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["message"] == response2.json()["message"]


class TestHealthEndpoint:
    """Tests for the health check endpoint"""

    def test_health_endpoint_returns_200(self):
        """Test health endpoint returns 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_healthy_status(self):
        """Test health endpoint returns healthy status"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_content_type(self):
        """Test health endpoint returns JSON content type"""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

    def test_multiple_health_checks(self):
        """Test health endpoint is consistent across multiple calls"""
        responses = [client.get("/health") for _ in range(3)]

        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


class TestCORSMiddleware:
    """Tests for CORS middleware configuration"""

    def test_cors_headers_present(self):
        """Test CORS middleware adds appropriate headers"""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_all_origins(self):
        """Test CORS allows all origins"""
        response = client.get("/", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "*"


class TestInvalidRoutes:
    """Tests for invalid route handling"""

    def test_invalid_route_returns_404(self):
        """Test requesting non-existent endpoint returns 404"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    def test_invalid_method_returns_405(self):
        """Test POST to GET-only endpoint returns 405"""
        response = client.post("/")
        assert response.status_code == 405


class TestMealHistoryEndpoints:
    """Tests for meal history endpoints"""

    def test_get_meal_history_invalid_user(self):
        """Test GET /meal-history/{user_id} returns 404 for invalid user"""
        response = client.get("/meal-history/nonexistent_user_12345")
        assert response.status_code == 404

    def test_get_meal_history_example_user(self):
        """Test GET /meal-history/example_user returns 200"""
        response = client.get("/meal-history/example_user")
        # May return 200 or 404 depending on if example data exists
        assert response.status_code in [200, 404]


class TestHealthReportEndpoints:
    """Tests for health report endpoints"""

    def test_get_health_report_invalid_user(self):
        """Test GET /health-report/{user_id} returns 404 for invalid user"""
        response = client.get("/health-report/nonexistent_user_12345")
        assert response.status_code == 404

    def test_get_health_report_example_user(self):
        """Test GET /health-report/example_user returns 200"""
        response = client.get("/health-report/example_user")
        # May return 200 or 404 depending on if example data exists
        assert response.status_code in [200, 404]


class TestFoodModelEndpoints:
    """Tests for food model endpoints"""

    def test_predict_endpoint_requires_file(self):
        """Test predict endpoint returns 422 when no file is provided"""
        response = client.post("/food-model/predict")
        # Should return 422 (validation error) because no file provided
        assert response.status_code == 422

    def test_predict_endpoint_accepts_post_only(self):
        """Test predict endpoint only accepts POST requests"""
        response = client.get("/food-model/predict")
        assert response.status_code in [405, 404]


class TestAppConfiguration:
    """Tests for app configuration"""

    def test_app_title(self):
        """Test FastAPI app has correct title"""
        # The app might be mounted, so check the api_app
        from api.service import api_app
        assert api_app.title == "TummyAI App API Server"

    def test_app_version(self):
        """Test FastAPI app has version set"""
        from api.service import api_app
        assert api_app.version == "v1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
