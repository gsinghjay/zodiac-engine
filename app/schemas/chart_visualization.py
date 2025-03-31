"""Schemas for chart visualization endpoints."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class NatalChartVisualizationRequest(BaseModel):
    """Schema for natal chart visualization request."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    city: Optional[str] = Field(None, description="City of birth")
    nation: Optional[str] = Field(None, description="Country of birth")
    lng: Optional[float] = Field(None, description="Longitude of birth place")
    lat: Optional[float] = Field(None, description="Latitude of birth place")
    tz_str: Optional[str] = Field(None, description="Timezone string (e.g., 'America/New_York')")
    houses_system: str = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")
    theme: str = Field("dark", description="Chart theme ('light', 'dark', 'dark-high-contrast', 'classic')")
    chart_language: str = Field("EN", description="Chart language ('EN', 'FR', 'PT', 'IT', 'CN', 'ES', 'RU', 'TR', 'DE', 'HI')")
    chart_id: Optional[str] = Field(None, description="Optional custom ID for the chart")

    class Config:
        json_schema_extra = {
            "example": {
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
                "chart_id": "john_doe_natal"
            }
        }

class SynastryChartVisualizationRequest(BaseModel):
    """Schema for synastry chart visualization request."""
    # First person
    name1: str = Field(..., description="Name of the first person")
    birth_date1: datetime = Field(..., description="Birth date and time of first person")
    city1: Optional[str] = Field(None, description="City of birth for first person")
    nation1: Optional[str] = Field(None, description="Country of birth for first person")
    lng1: Optional[float] = Field(None, description="Longitude of birth place for first person")
    lat1: Optional[float] = Field(None, description="Latitude of birth place for first person")
    tz_str1: Optional[str] = Field(None, description="Timezone string for first person")
    
    # Second person
    name2: str = Field(..., description="Name of the second person")
    birth_date2: datetime = Field(..., description="Birth date and time of second person")
    city2: Optional[str] = Field(None, description="City of birth for second person")
    nation2: Optional[str] = Field(None, description="Country of birth for second person")
    lng2: Optional[float] = Field(None, description="Longitude of birth place for second person")
    lat2: Optional[float] = Field(None, description="Latitude of birth place for second person")
    tz_str2: Optional[str] = Field(None, description="Timezone string for second person")
    
    # Shared settings
    houses_system: str = Field("P", description="House system identifier")
    theme: str = Field("dark", description="Chart theme")
    chart_language: str = Field("EN", description="Chart language")
    chart_id: Optional[str] = Field(None, description="Optional custom ID for the chart")

    class Config:
        json_schema_extra = {
            "example": {
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
                "chart_id": "john_jane_synastry"
            }
        }

class ChartVisualizationResponse(BaseModel):
    """Schema for chart visualization response."""
    chart_id: str = Field(..., description="ID of the generated chart")
    svg_url: str = Field(..., description="URL to access the SVG visualization")

    class Config:
        json_schema_extra = {
            "example": {
                "chart_id": "natal_12345678",
                "svg_url": "/static/images/charts/natal_12345678"
            }
        } 