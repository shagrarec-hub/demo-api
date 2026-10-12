"""
Tests for the Flask API.

Run with:
    pip install pytest
    pytest test_app.py
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data
    assert "timestamp" in data


def test_get_data(client):
    """Test the /api/data endpoint."""
    response = client.get("/api/data")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Flask API"
    assert len(data["items"]) == 3


def test_get_data_with_limit(client):
    """Test /api/data with limit parameter."""
    response = client.get("/api/data?limit=2")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["items"]) == 2


def test_get_data_with_invalid_limit(client):
    """Test /api/data with invalid limit parameter."""
    response = client.get("/api/data?limit=-1")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "message" in data


def test_not_found(client):
    """Test 404 error handling."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "not_found"


def test_method_not_allowed(client):
    """Test 405 error handling."""
    response = client.post("/health")
    assert response.status_code == 405
    data = response.get_json()
    assert data["error"] == "method_not_allowed"
