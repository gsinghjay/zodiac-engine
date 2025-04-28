"""Schemas for chart visualization endpoints."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# Based on the Kerykeion literals
ZodiacType = Literal["Tropic", "Sidereal"]
SiderealMode = Literal[
    "FAGAN_BRADLEY", "LAHIRI", "DELUCE", "RAMAN", "USHASHASHI", "KRISHNAMURTI", 
    "DJWHAL_KHUL", "YUKTESHWAR", "JN_BHASIN", "BABYL_KUGLER1", "BABYL_KUGLER2", 
    "BABYL_KUGLER3", "BABYL_HUBER", "BABYL_ETPSC", "ALDEBARAN_15TAU", "HIPPARCHOS", 
    "SASSANIAN", "J2000", "J1900", "B1950"
]

PerspectiveType = Literal["Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric"]

Planet = Literal[
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
    "Neptune", "Pluto", "Mean_Node", "True_Node", "Mean_South_Node", "True_South_Node", 
    "Chiron", "Mean_Lilith"
]

AxialCusps = Literal["Ascendant", "Medium_Coeli", "Descendant", "Imum_Coeli"]

AspectName = Literal[
    "conjunction", "semi-sextile", "semi-square", "sextile", "quintile", 
    "square", "trine", "sesquiquadrate", "biquintile", "quincunx", "opposition"
]

class AspectConfiguration(BaseModel):
    """Schema for aspect configuration."""
    name: AspectName = Field(..., description="Name of the aspect")
    orb: float = Field(..., description="Orb value for the aspect in degrees")

class ChartConfiguration(BaseModel):
    """Schema for chart configuration options."""
    houses_system: str = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")
    zodiac_type: ZodiacType = Field("Tropic", description="Zodiac type: Tropic (default) or Sidereal")
    sidereal_mode: SiderealMode | None = Field(None, description="Sidereal mode (required if zodiac_type is Sidereal)")
    perspective_type: PerspectiveType = Field("Apparent Geocentric", description="Type of perspective for calculations")
    active_points: list[Planet | AxialCusps] = Field(
        default=[
            "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
            "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
            "Mean_Lilith", "Mean_South_Node"
        ],
        description="List of active planets and points to include in the chart"
    )
    active_aspects: list[AspectConfiguration] = Field(
        default=[
            {"name": "conjunction", "orb": 10}, 
            {"name": "opposition", "orb": 10}, 
            {"name": "trine", "orb": 8}, 
            {"name": "sextile", "orb": 6}, 
            {"name": "square", "orb": 5}, 
            {"name": "quintile", "orb": 1}
        ],
        description="List of active aspects with their orbs"
    )

class NatalChartVisualizationRequest(BaseModel):
    """Schema for natal chart visualization request."""
    name: str = Field(..., description="Name of the person")
    birth_date: str = Field(..., description="Birth date and time in ISO format")
    city: str | None = Field(None, description="City of birth")
    nation: str | None = Field(None, description="Country of birth")
    lng: float | None = Field(None, description="Longitude of birth place")
    lat: float | None = Field(None, description="Latitude of birth place")
    tz_str: str | None = Field(None, description="Timezone string (e.g., 'America/New_York')")
    chart_id: str | None = Field(None, description="Optional custom ID for the chart")
    
    # Visualization options
    theme: str = Field("dark", description="Chart theme ('light', 'dark', 'dark-high-contrast', 'classic')")
    language: str = Field("EN", description="Chart language ('EN', 'FR', 'PT', 'IT', 'CN', 'ES', 'RU', 'TR', 'DE', 'HI')")
    
    # Chart configuration
    config: ChartConfiguration | None = Field(None, description="Chart configuration options")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "birth_date": "1990-01-01T12:00:00",
                "city": "New York",
                "nation": "US",
                "lng": -74.006,
                "lat": 40.7128,
                "tz_str": "America/New_York",
                "chart_id": "john_doe_natal",
                "theme": "dark",
                "language": "EN",
                "config": {
                    "houses_system": "P",
                    "zodiac_type": "Tropic",
                    "perspective_type": "Apparent Geocentric",
                    "active_points": [
                        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
                        "Uranus", "Neptune", "Pluto", "Ascendant", "Medium_Coeli"
                    ],
                    "active_aspects": [
                        {"name": "conjunction", "orb": 8},
                        {"name": "opposition", "orb": 8},
                        {"name": "trine", "orb": 6},
                        {"name": "square", "orb": 6}
                    ]
                }
                }
            }
        }

class SynastryChartVisualizationRequest(BaseModel):
    """Schema for synastry chart visualization request."""
    # First person
    name1: str = Field(..., description="Name of the first person")
    birth_date1: str = Field(..., description="Birth date and time of first person in ISO format")
    city1: str | None = Field(None, description="City of birth for first person")
    nation1: str | None = Field(None, description="Country of birth for first person")
    lng1: float | None = Field(None, description="Longitude of birth place for first person")
    lat1: float | None = Field(None, description="Latitude of birth place for first person")
    tz_str1: str | None = Field(None, description="Timezone string for first person")
    
    # Second person
    name2: str = Field(..., description="Name of the second person")
    birth_date2: str = Field(..., description="Birth date and time of second person in ISO format")
    city2: str | None = Field(None, description="City of birth for second person")
    nation2: str | None = Field(None, description="Country of birth for second person")
    lng2: float | None = Field(None, description="Longitude of birth place for second person")
    lat2: float | None = Field(None, description="Latitude of birth place for second person")
    tz_str2: str | None = Field(None, description="Timezone string for second person")
    
    # Shared settings
    chart_id: str | None = Field(None, description="Optional custom ID for the chart")
    theme: str = Field("dark", description="Chart theme")
    language: str = Field("EN", description="Chart language")
    
    # Chart configuration
    config: ChartConfiguration | None = Field(None, description="Chart configuration options")

    model_config = {
        "json_schema_extra": {
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
                
                "chart_id": "john_jane_synastry",
                "theme": "dark",
                "language": "EN",
                "config": {
                    "houses_system": "P",
                    "zodiac_type": "Tropic",
                    "perspective_type": "Apparent Geocentric",
                    "active_points": ["Sun", "Moon", "Venus", "Mars", "Ascendant"],
                    "active_aspects": [
                        {"name": "conjunction", "orb": 6},
                        {"name": "opposition", "orb": 6}, 
                        {"name": "trine", "orb": 5}
                    ]
                }
                }
            }
        }

class ChartVisualizationResponse(BaseModel):
    """Schema for chart visualization response."""
    chart_id: str = Field(..., description="ID of the generated chart")
    svg_url: str = Field(..., description="URL to access the SVG visualization")

    model_config = {
        "json_schema_extra": {
            "example": {
                "chart_id": "natal_12345678",
                "svg_url": "/static/images/svg/natal_12345678.svg"
            }
            }
        }

class NatalChartVisualizationResponse(ChartVisualizationResponse):
    """Response schema for natal chart visualization."""
    pass

class SynastryChartVisualizationResponse(ChartVisualizationResponse):
    """Response schema for synastry chart visualization."""
    pass 