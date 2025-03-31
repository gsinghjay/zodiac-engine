"""Tests for static images routes."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_chart_svg_success():
    """Test retrieving a chart SVG image that exists."""
    response = client.get("/static/images/charts/sample")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert "Sample Astrological Chart" in response.text
    assert "<svg" in response.text

def test_get_chart_svg_not_found():
    """Test retrieving a chart SVG image that doesn't exist."""
    response = client.get("/static/images/charts/nonexistent")
    assert response.status_code == 404 