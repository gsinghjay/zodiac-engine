"""Schemas for natal chart calculations."""
from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

class PlanetPosition(BaseModel):
    """Schema for planet position in natal chart."""
    name: str = Field(..., description="Name of the planet")
    sign: str = Field(..., description="Zodiac sign the planet is in")
    position: float = Field(..., description="Position in degrees")
    house: Union[int, str] = Field(..., description="House number or name")
    retrograde: bool = Field(..., description="Whether the planet is retrograde")

class NatalChartRequest(BaseModel):
    """Schema for natal chart calculation request."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    city: Optional[str] = Field(None, description="City of birth")
    nation: Optional[str] = Field(None, description="Country of birth")
    lng: Optional[float] = Field(None, description="Longitude of birth place")
    lat: Optional[float] = Field(None, description="Latitude of birth place")
    tz_str: Optional[str] = Field(None, description="Timezone string (e.g., 'America/New_York')")
    houses_system: Optional[str] = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")

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
                "houses_system": "P"
            }
        }

class AspectInfo(BaseModel):
    """Schema for planetary aspect information."""
    p1_name: str = Field(..., description="Name of first planet")
    p2_name: str = Field(..., description="Name of second planet")
    aspect: str = Field(..., description="Type of aspect")
    orbit: float = Field(..., description="Orbital degree of aspect")

class HouseSystem(BaseModel):
    """Schema for house system information."""
    name: str = Field(..., description="Full name of the house system")
    identifier: str = Field(..., description="Single letter identifier of the house system")

class NatalChartResponse(BaseModel):
    """Schema for natal chart calculation response."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    planets: List[PlanetPosition] = Field(..., description="List of planet positions")
    houses: Dict[int, float] = Field(..., description="House cusps positions")
    aspects: List[AspectInfo] = Field(..., description="List of planetary aspects")
    house_system: HouseSystem = Field(..., description="House system used for calculations") 