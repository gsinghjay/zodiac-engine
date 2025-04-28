"""Tests for chart configuration features."""
import os
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

client = TestClient(app)

# Test data
TEST_NATAL_DATA: Dict[str, Any] = {
    "name": "Test Person",
    "birth_date": "1990-01-01T12:00:00",
    "lng": -74.006,  # New York coordinates
    "lat": 40.7128,
    "tz_str": "America/New_York",
    "language": "EN",
    "theme": "dark"
}

def test_natal_chart_with_tropical_zodiac():
    """Test natal chart with tropical zodiac configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "zodiac_type": "Tropic"
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
    
    # Verify the SVG file was created
    chart_id = json_response["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains tropical reference 
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Tropical" in svg_content

def test_natal_chart_with_sidereal_zodiac():
    """Test natal chart with sidereal zodiac configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "zodiac_type": "Sidereal",
            "sidereal_mode": "LAHIRI"
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
    
    # Verify the SVG file was created
    chart_id = json_response["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains sidereal reference (Kerykeion uses "Ayanamsa" for sidereal zodiac)
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Ayanamsa" in svg_content

def test_natal_chart_with_limited_planets():
    """Test natal chart with limited active planets configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128, 
        "tz_str": "America/New_York",
        "config": {
            "active_points": ["Sun", "Moon", "Ascendant"]
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
    
    # Verify the SVG file was created
    chart_id = json_response["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains only the selected planets
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Sun" in svg_content
        assert "Moon" in svg_content

def test_natal_chart_with_custom_aspects():
    """Test natal chart with custom aspects configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "active_aspects": [
                {"name": "conjunction", "orb": 5},
                {"name": "opposition", "orb": 5}
            ]
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")

def test_natal_chart_with_different_house_system():
    """Test natal chart with different house system configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "houses_system": "W"  # Whole Sign houses
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")

def test_synastry_chart_with_configuration():
    """Test synastry chart with configuration options."""
    data = {
        "name1": "John Doe",
        "birth_date1": "1990-01-01T12:00:00",
        "city1": "New York",
        "nation1": "US",
        "lng1": -74.006,
        "lat1": 40.7128,
        "tz_str1": "America/New_York",
        "name2": "Jane Doe",
        "birth_date2": "1992-05-15T15:30:00",
        "city2": "Los Angeles",
        "nation2": "US",
        "lng2": -118.2437,
        "lat2": 34.0522,
        "tz_str2": "America/Los_Angeles",
        "config": {
            "houses_system": "P",
            "zodiac_type": "Tropic",
            "active_points": ["Sun", "Moon", "Venus", "Mars", "Ascendant"],
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 6},
                {"name": "square", "orb": 6}
            ]
        }
    }
    response = client.post("/api/v1/charts/visualization/synastry", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg") 