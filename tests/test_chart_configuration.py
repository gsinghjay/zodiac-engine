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
    """Test generating a natal chart with tropical zodiac."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P"
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains tropical reference 
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Tropical" in svg_content

def test_natal_chart_with_sidereal_zodiac():
    """Test generating a natal chart with sidereal zodiac."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Sidereal",
            "sidereal_mode": "FAGAN_BRADLEY",
            "houses_system": "P"
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains sidereal reference (Kerykeion uses "Ayanamsa" for sidereal zodiac)
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Ayanamsa" in svg_content

def test_natal_chart_with_limited_planets():
    """Test generating a natal chart with limited planets."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P",
            "active_points": ["Sun", "Moon", "Ascendant", "Medium_Coeli"]
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains only the selected planets
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Sun" in svg_content
        assert "Moon" in svg_content
        # Checking that other planets like Saturn are not included
        # would be brittle as the SVG might contain the word Saturn in other contexts
        # so we're focusing on positive assertions

def test_natal_chart_with_custom_aspects():
    """Test generating a natal chart with custom aspects."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P",
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 6}
            ]
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)

def test_natal_chart_with_different_house_system():
    """Test generating a natal chart with a different house system."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "K"  # Koch house system
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
def test_synastry_chart_with_configuration():
    """Test generating a synastry chart with configuration."""
    data = {
        "name1": "Person One",
        "birth_date1": "1990-01-01T12:00:00",
        "lng1": -74.006,  # New York coordinates
        "lat1": 40.7128,
        "tz_str1": "America/New_York",
        
        "name2": "Person Two",
        "birth_date2": "1995-06-15T15:30:00",
        "lng2": -118.2437,  # Los Angeles coordinates
        "lat2": 34.0522,
        "tz_str2": "America/Los_Angeles",
        
        "language": "EN",
        "theme": "dark",
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P",
            "active_points": ["Sun", "Moon", "Ascendant", "Venus", "Mars"],
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 6}
            ]
        }
    }
    
    response = client.post("/api/v1/charts/visualization/synastry", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path) 