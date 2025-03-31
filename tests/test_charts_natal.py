from datetime import datetime
from typing import Dict

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture
def valid_natal_chart_request() -> Dict:
    """Fixture for valid natal chart request data."""
    return {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York"
    }

def test_calculate_natal_chart_success(valid_natal_chart_request):
    """Test successful natal chart calculation with new chart endpoint."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "name" in data
    assert "birth_date" in data
    assert "planets" in data
    assert "houses" in data
    assert "aspects" in data
    
    # Check planets data
    assert len(data["planets"]) > 0
    for planet in data["planets"]:
        assert "name" in planet
        assert "sign" in planet
        assert "position" in planet
        assert "house" in planet
        assert "retrograde" in planet
    
    # Check houses data
    assert len(data["houses"]) == 12
    
    # Check aspects data
    assert isinstance(data["aspects"], list)

def test_calculate_natal_chart_invalid_date():
    """Test natal chart calculation with invalid date."""
    invalid_request = {
        "name": "John Doe",
        "birth_date": "invalid-date",
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/natal/", json=invalid_request)
    assert response.status_code == 422

def test_calculate_natal_chart_missing_required():
    """Test natal chart calculation with missing required fields."""
    invalid_request = {
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/natal/", json=invalid_request)
    assert response.status_code == 422

def test_calculate_natal_chart_coordinates_only(valid_natal_chart_request):
    """Test natal chart calculation with coordinates only."""
    request = {
        "name": valid_natal_chart_request["name"],
        "birth_date": valid_natal_chart_request["birth_date"],
        "lng": valid_natal_chart_request["lng"],
        "lat": valid_natal_chart_request["lat"],
        "tz_str": valid_natal_chart_request["tz_str"]
    }
    
    response = client.post("/api/v1/charts/natal/", json=request)
    assert response.status_code == 200 