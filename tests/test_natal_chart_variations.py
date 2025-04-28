"""Tests for various natal chart variations."""
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
    "tz_str": "America/New_York"
}

def test_natal_chart_different_themes():
    """Test generating natal charts with different themes."""
    themes = ["light", "dark", "dark-high-contrast", "classic"]
    
    for theme in themes:
        data = {
            **TEST_NATAL_DATA,
            "theme": theme,
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

def test_natal_chart_different_languages():
    """Test generating natal charts with different languages."""
    languages = ["EN", "FR", "IT", "ES", "DE"]  # Using a subset of languages for testing
    
    for language in languages:
        data = {
            **TEST_NATAL_DATA,
            "language": language,
            "theme": "dark",
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

def test_natal_chart_different_perspective_types():
    """Test generating natal charts with different perspective types."""
    perspective_types = ["Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric"]
    
    for perspective_type in perspective_types:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P",
                "perspective_type": perspective_type
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
        
        # Verify the perspective type is shown in the chart
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert perspective_type in svg_content or perspective_type.replace(" ", "_").lower() in svg_content.lower()

def test_natal_chart_different_sidereal_modes():
    """Test generating natal charts with different sidereal modes."""
    sidereal_modes = ["FAGAN_BRADLEY", "LAHIRI", "DELUCE", "KRISHNAMURTI", "DJWHAL_KHUL"]
    
    for sidereal_mode in sidereal_modes:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Sidereal",
                "sidereal_mode": sidereal_mode,
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
        
        # Verify the SVG file contains Ayanamsa reference
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert "Ayanamsa" in svg_content

def test_natal_chart_different_celestial_points():
    """Test generating natal charts with different celestial points."""
    point_sets = [
        ["Sun", "Moon", "Mercury", "Venus", "Mars"],  # Basic planets
        ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"],  # All planets
        ["Sun", "Moon", "Ascendant", "Medium_Coeli", "Descendant", "Imum_Coeli"],  # Main points + angles
        ["Sun", "Moon", "Chiron", "Mean_Lilith", "Mean_Node", "True_Node"],  # Special points
    ]
    
    for points in point_sets:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P",
                "active_points": points
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
        
        # Verify at least one of the specified points appears in the content
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert any(point in svg_content for point in points)

def test_natal_chart_different_house_systems():
    """Test generating natal charts with different house systems."""
    # Valid house systems from the error message:
    # 'A', 'B', 'C', 'D', 'F', 'H', 'I', 'i', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'
    house_systems = ["P", "K", "C", "R", "W", "B", "M", "A", "D"]  # Placidus, Koch, Campanus, Regiomontanus, Whole Sign, Alcabitius, Morinus, Equal, Equal
    
    for house_system in house_systems:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": house_system
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