from datetime import datetime
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture
def valid_natal_chart_request() -> Dict[str, Any]:
    """Fixture for valid natal chart request data."""
    return {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "houses_system": "P"  # Default to Placidus
    }

def test_calculate_natal_chart_success(valid_natal_chart_request):
    """Test successful natal chart calculation with new chart endpoint."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check response structure
    assert "name" in data
    assert "birth_date" in data
    assert "planets" in data
    assert "houses" in data
    assert "aspects" in data
    assert "house_system" in data
    
    # Check house system data
    assert "name" in data["house_system"]
    assert "identifier" in data["house_system"]
    assert data["house_system"]["identifier"] == valid_natal_chart_request["houses_system"]
    
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
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_calculate_natal_chart_missing_required():
    """Test natal chart calculation with missing required fields."""
    invalid_request = {
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/natal/", json=invalid_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_calculate_natal_chart_coordinates_only(valid_natal_chart_request):
    """Test natal chart calculation with coordinates only."""
    request = {
        "name": valid_natal_chart_request["name"],
        "birth_date": valid_natal_chart_request["birth_date"],
        "lng": valid_natal_chart_request["lng"],
        "lat": valid_natal_chart_request["lat"],
        "tz_str": valid_natal_chart_request["tz_str"],
        "houses_system": valid_natal_chart_request["houses_system"]
    }
    
    response = client.post("/api/v1/charts/natal/", json=request)
    assert response.status_code == status.HTTP_200_OK

def test_calculate_natal_chart_celestial_points(valid_natal_chart_request):
    """Test that all celestial points are included in the response."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Get all planet names from the response
    planet_names = [planet["name"].lower() for planet in data["planets"]]
    
    # Check for standard planets
    standard_planets = ["sun", "moon", "mercury", "venus", "mars", 
                       "jupiter", "saturn", "uranus", "neptune", "pluto"]
    for planet in standard_planets:
        assert planet in planet_names, f"{planet} is missing from the response"
    
    # Check for additional required celestial points
    required_points = ["mean node", "true node", "mean lilith", "chiron"]
    for point in required_points:
        assert any(point in p for p in planet_names), f"{point} is missing from the response"

def test_calculate_natal_chart_aspect_data(valid_natal_chart_request):
    """Test that aspect data includes complete information with orbs."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify we have aspects
    assert len(data["aspects"]) > 0
    
    # Check aspect structure and orb information
    for aspect in data["aspects"]:
        assert "p1_name" in aspect
        assert "p2_name" in aspect
        assert "aspect" in aspect
        assert "orbit" in aspect
        assert isinstance(aspect["orbit"], (int, float))

def test_calculate_natal_chart_different_house_system(valid_natal_chart_request):
    """Test natal chart calculation with a different house system."""
    # Clone the request and change house system to Whole Sign
    request = valid_natal_chart_request.copy()
    request["houses_system"] = "W"  # Whole Sign
    
    response = client.post("/api/v1/charts/natal/", json=request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify the house system in the response
    assert data["house_system"]["identifier"] == "W"
    
    # House systems have different names
    assert data["house_system"]["name"] != "Placidus" 