"""
Integration tests for the TummyAI App API
Tests the full API endpoints with FastAPI TestClient
"""

import pytest
import pandas as pd
from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.service import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


class TestAPIEndpoints:
    """Integration tests for API endpoints"""

    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "TummyAI app" in data["message"]

    def test_root_returns_json(self):
        """Test that root returns JSON content type"""
        response = client.get("/")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

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


class TestMealHistoryAPIEndpoints:
    """Integration tests for Meal History API endpoints"""

    def test_get_meal_history_simple(self):
        """Test GET /meal-history/{user_id} endpoint with simple CSV"""
        user_id = "testuser"

        # Sample data
        sample_df = [
            {"id": 1, "ingredients": ["milk", "cheese"], "symptoms": ["nausea"]},
            {"id": 2, "ingredients": ["bread"], "symptoms": ["headache", "nausea"]},
        ]

        # Patch get_blob and read_csv_from_gcs to return sample data
        with (
            patch("api.routers.meal_history.get_blob") as mock_get_blob,
            patch("api.routers.meal_history.read_csv_from_gcs") as mock_read_csv,
        ):
            mock_blob = MagicMock()
            mock_get_blob.return_value = mock_blob
            mock_read_csv.return_value = pd.DataFrame(sample_df)

            response = client.get(f"/meal-history/{user_id}")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == len(sample_df)
            assert data == sample_df

    def test_get_meal_history_not_found(self):
        """Test GET /meal-history/{user_id} endpoint when file not found"""
        user_id = "nonexistentuser"

        with patch("api.routers.meal_history.get_blob") as mock_get_blob:
            mock_get_blob.side_effect = HTTPException(status_code=404, detail="File not found")

            response = client.get(f"/meal-history/{user_id}")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "File not found"

    def test_put_meal_history_simple(self):
        """Test PUT /meal-history/{user_id} endpoint with simple data"""
        user_id = "testuser"
        new_meal = {"date_time": "2025-01-02 12:00:00", "ingredients": "bread", "symptoms": "headache,nausea"}

        # Existing data
        existing_df = pd.DataFrame(
            [{"date_time": "2025-01-01 12:00:00", "ingredients": "milk,cheese", "symptoms": "nausea"}]
        )

        # Patch get_blob, read_csv_from_gcs, and write_csv_to_gcs
        with (
            patch("api.routers.meal_history.get_blob") as mock_get_blob,
            patch("api.routers.meal_history.read_csv_from_gcs") as mock_read_csv,
            patch("api.routers.meal_history.write_csv_to_gcs") as mock_write_csv,
        ):
            mock_blob = MagicMock()
            mock_blob.name = "meal_history_testuser.csv"
            mock_get_blob.return_value = mock_blob
            mock_read_csv.return_value = existing_df
            mock_write_csv.return_value = None

            response = client.put(f"/meal-history/{user_id}", json=new_meal)

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["user_id"] == user_id
            assert data["file"] == mock_blob.name

            written_df = mock_write_csv.call_args[0][1]
            assert len(written_df) == 2
            assert new_meal["ingredients"] in written_df["ingredients"].values
            assert new_meal["symptoms"] in written_df["symptoms"].values

    def test_put_meal_history_not_found(self):
        """Test PUT /meal-history/{user_id} endpoint when file not found"""
        user_id = "nonexistentuser"
        new_meal = {"date_time": "2025-01-02 12:00:00", "ingredients": "bread", "symptoms": "headache,nausea"}

        with patch("api.routers.meal_history.get_blob") as mock_get_blob:
            mock_get_blob.side_effect = HTTPException(status_code=404, detail="File not found")

            response = client.put(f"/meal-history/{user_id}", json=new_meal)

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "File not found"


class TestHealthReportAPIEndpoints:
    """Integration tests for Health Report API endpoints"""

    def test_get_health_report_simple(self):
        """Test GET /health-report/{user_id} endpoint with simple data"""
        user_id = "testuser"

        # Sample health report CSV data
        sample_df = pd.DataFrame(
            [
                {
                    "symptom": "headache",
                    "ingredient": "milk",
                    "odds_ratio": 1.5,
                    "p_value": 0.04,
                    "p_value_adj": 0.05,
                    "significant": True,
                },
                {
                    "symptom": "nausea",
                    "ingredient": "cheese",
                    "odds_ratio": 2.0,
                    "p_value": 0.01,
                    "p_value_adj": 0.02,
                    "significant": False,
                },
            ]
        )

        # Patch GCS functions
        with (
            patch("api.routers.health_report.get_blob") as mock_get_blob,
            patch("api.routers.health_report.read_csv_from_gcs") as mock_read_csv,
        ):
            mock_blob = MagicMock()
            mock_blob.name = "health_report_testuser.csv"
            mock_get_blob.return_value = mock_blob
            mock_read_csv.return_value = sample_df

            response = client.get(f"/health-report/{user_id}")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == len(sample_df)
            for i, row in enumerate(sample_df.to_dict(orient="records")):
                assert data[i] == row

    def test_get_health_report_not_found(self):
        """Test GET /health-report/{user_id} endpoint when file not found"""
        user_id = "nonexistentuser"

        with patch("api.routers.health_report.get_blob") as mock_get_blob:
            mock_get_blob.side_effect = HTTPException(status_code=404, detail="File not found")

            response = client.get(f"/health-report/{user_id}")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "File not found"

    def test_put_health_report_simple(self):
        """Test PUT /health-report/{user_id} endpoint with simple data"""
        user_id = "testuser"

        # Sample meal history data returned from GCS
        sample_history = pd.DataFrame(
            [
                {"date_time": "2025-01-01 12:00:00", "ingredients": "milk,cheese", "symptoms": "nausea"},
                {"date_time": "2025-01-02 12:00:00", "ingredients": "bread", "symptoms": "headache,nausea"},
            ]
        )

        # Sample health report returned after processing
        sample_report = pd.DataFrame(
            [
                {
                    "symptom": "headache",
                    "ingredient": "bread",
                    "odds_ratio": 1.5,
                    "p_value": 0.04,
                    "p_value_adj": 0.05,
                    "significant": True,
                },
                {
                    "symptom": "nausea",
                    "ingredient": "milk",
                    "odds_ratio": 2.0,
                    "p_value": 0.01,
                    "p_value_adj": 0.02,
                    "significant": False,
                },
            ]
        )

        # Patch GCS interactions and processing functions
        with (
            patch("api.routers.health_report.get_blob") as mock_get_blob,
            patch("api.routers.health_report.read_csv_from_gcs") as mock_read_csv,
            patch("api.routers.health_report.write_csv_to_gcs") as mock_write_csv,
            patch("api.routers.health_report.convert_onehot") as mock_convert_onehot,
            patch("api.routers.health_report.run_fisher") as mock_run_fisher,
        ):

            mock_history_blob = MagicMock()
            mock_report_blob = MagicMock()
            mock_report_blob.name = f"data/health_report/health_report_{user_id}.csv"

            mock_get_blob.side_effect = [mock_history_blob, mock_report_blob]
            mock_read_csv.return_value = sample_history
            mock_convert_onehot.return_value = sample_history
            mock_run_fisher.return_value = sample_report
            mock_write_csv.return_value = None

            response = client.put(f"/health-report/{user_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["user_id"] == user_id
            assert data["file"] == f"data/health_report/health_report_{user_id}.csv"

    def test_put_health_report_not_found(self):
        """Test PUT /health-report/{user_id} endpoint when meal history file not found"""
        user_id = "nonexistentuser"

        with patch("api.routers.health_report.get_blob") as mock_get_blob:
            mock_get_blob.side_effect = HTTPException(status_code=404, detail="File not found")

            response = client.put(f"/health-report/{user_id}")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "File not found"
