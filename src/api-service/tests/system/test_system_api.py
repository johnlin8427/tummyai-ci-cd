"""
System tests for FastAPI endpoints
Tests the actual API endpoints with HTTP requests
"""

import pytest
import requests
import pandas as pd
import numpy as np


# Base URL for the API (assumes API is running)
API_BASE_URL = "http://localhost:9000"


def is_api_running():
    """Check if API is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@pytest.mark.skipif(not is_api_running(), reason="API not running at localhost:9000")
class TestAPIEndpoints:
    """Integration tests for API endpoints"""

    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message"""
        response = requests.get(f"{API_BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "TummyAI app" in data["message"]

    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_get_meal_history_example(self):
        """Test the /meal-history/example endpoint"""
        response = requests.get(f"{API_BASE_URL}/meal-history/example")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        record = data[0]
        assert "date_time" in record
        assert "ingredients" in record
        assert "symptoms" in record

    def test_get_meal_history_not_found(self):
        """Test the /meal-history endpoint when file not found"""
        response = requests.get(f"{API_BASE_URL}/meal-history/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "File not found" in data["detail"]

    def test_put_meal_history_example(self):
        """Test putting to /meal-history/example endpoint"""
        new_record = {"date_time": "2025-01-01 12:00:00", "ingredients": "milk,cheese", "symptoms": "nausea"}
        response = requests.put(f"{API_BASE_URL}/meal-history/example", json=new_record)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["user_id"] == "example"
        assert data["file"] == "data/meal_history/meal_history_example.csv"

    def test_put_meal_history_not_found(self):
        """Test putting to /meal-history endpoint when file not found"""
        new_record = {"date_time": "2025-01-01 12:00:00", "ingredients": "milk,cheese", "symptoms": "nausea"}
        response = requests.put(f"{API_BASE_URL}/meal-history/nonexistent", json=new_record)
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "File not found" in data["detail"]

    def test_get_health_report_example(self):
        """Test the /health-report/example endpoint"""
        response = requests.get(f"{API_BASE_URL}/health-report/health_report_example_user")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        record = pd.DataFrame(data)
        expected_columns = {
            "symptom": str,
            "ingredient": str,
            "odds_ratio": float,
            "p_value": float,
            "p_value_adj": float,
            "significant": np.bool_,
        }
        for col, type in expected_columns.items():
            assert col in record.columns
            assert isinstance(record[col].iloc[0], type)

    def test_get_health_report_not_found(self):
        """Test the /health-report endpoint when file not found"""
        response = requests.get(f"{API_BASE_URL}/health-report/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "File not found" in data["detail"]

    def test_put_health_report_example(self):
        """Test putting to /health-report/example endpoint"""
        response = requests.put(f"{API_BASE_URL}/health-report/health_report_example_user")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["user_id"] == "example"
        assert data["report_file"] == "data/health_report/health_report_example_user.csv"

    def test_put_health_report_not_found(self):
        """Test putting to /health-report endpoint when file not found"""
        response = requests.put(f"{API_BASE_URL}/health-report/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "File not found" in data["detail"]


# Standalone tests that don't require running API
class TestAPIWithoutServer:
    """Tests that can run without a live server"""

    def test_api_structure(self):
        """Test that we can import the API module"""
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "api-service"))

        from api.service import app

        assert app.title == "TummyAI App API Server"
        assert app.version == "v1"
