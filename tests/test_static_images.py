"""Tests for static images routes."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_chart_svg_success():
    """Test retrieving a chart SVG image that exists."""
    response = client.get("/static/images/svg/sample.svg")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert "Sample Astrological Chart" in response.text
    assert "<svg" in response.text

def test_get_chart_svg_not_found():
    """Test retrieving a chart SVG image that doesn't exist."""
    response = client.get("/static/images/svg/nonexistent.svg")
    assert response.status_code == 404

@pytest.fixture
def valid_natal_visualization_request():
    """Fixture for valid natal chart visualization request."""
    return {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "houses_system": "P",
        "theme": "dark",
        "chart_language": "EN",
        "chart_id": "test_natal_chart"
    }

@pytest.fixture
def valid_synastry_visualization_request():
    """Fixture for valid synastry chart visualization request."""
    return {
        "name1": "John Doe",
        "birth_date1": "1990-01-01T12:00:00",
        "city1": "New York",
        "nation1": "US",
        "lng1": -74.006,
        "lat1": 40.7128,
        "tz_str1": "America/New_York",
        
        "name2": "Jane Smith",
        "birth_date2": "1992-03-15T15:30:00",
        "city2": "Los Angeles",
        "nation2": "US",
        "lng2": -118.2437,
        "lat2": 34.0522,
        "tz_str2": "America/Los_Angeles",
        
        "houses_system": "P",
        "theme": "dark",
        "chart_language": "EN",
        "chart_id": "test_synastry_chart"
    }

def test_generate_natal_chart_visualization(valid_natal_visualization_request):
    """Test generating a natal chart visualization."""
    response = client.post(
        "/api/v1/charts/visualization/natal", 
        json=valid_natal_visualization_request
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "chart_id" in data
    assert "svg_url" in data
    
    # Check that the values match what we expect
    assert data["chart_id"] == valid_natal_visualization_request["chart_id"]
    assert data["svg_url"] == f"/static/images/svg/{valid_natal_visualization_request['chart_id']}.svg"
    
    # Verify we can retrieve the generated SVG
    svg_response = client.get(data["svg_url"])
    assert svg_response.status_code == 200
    assert svg_response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in svg_response.text

def test_generate_synastry_chart_visualization(valid_synastry_visualization_request):
    """Test generating a synastry chart visualization."""
    response = client.post(
        "/api/v1/charts/visualization/synastry", 
        json=valid_synastry_visualization_request
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "chart_id" in data
    assert "svg_url" in data
    
    # Check that the values match what we expect
    assert data["chart_id"] == valid_synastry_visualization_request["chart_id"]
    assert data["svg_url"] == f"/static/images/svg/{valid_synastry_visualization_request['chart_id']}.svg"
    
    # Verify we can retrieve the generated SVG
    svg_response = client.get(data["svg_url"])
    assert svg_response.status_code == 200
    assert svg_response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in svg_response.text

def test_generate_natal_chart_missing_required_fields():
    """Test generating a natal chart visualization with missing required fields."""
    incomplete_request = {
        "name": "John Doe"
        # Missing birth_date
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=incomplete_request)
    assert response.status_code == 422  # Validation error

def test_generate_natal_chart_invalid_date():
    """Test generating a natal chart visualization with invalid date."""
    invalid_request = {
        "name": "John Doe",
        "birth_date": "invalid-date",
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=invalid_request)
    assert response.status_code == 422  # Validation error 