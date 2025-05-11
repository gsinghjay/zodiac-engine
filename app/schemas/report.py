"""Schemas for astrological reports."""
from datetime import datetime
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field

# Report Request Schemas
class NatalReportRequest(BaseModel):
    """Schema for natal chart report request."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    city: str | None = Field(None, description="City of birth")
    nation: str | None = Field(None, description="Country of birth")
    lng: float | None = Field(None, description="Longitude of birth place")
    lat: float | None = Field(None, description="Latitude of birth place")
    tz_str: str | None = Field(None, description="Timezone string (e.g., 'America/New_York')")
    houses_system: str | None = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")

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
                "houses_system": "P"
            }
        }
    }

class SynastryReportRequest(BaseModel):
    """Schema for synastry report request."""
    name1: str = Field(..., description="Name of the first person")
    birth_date1: datetime = Field(..., description="Birth date and time of the first person")
    city1: str | None = Field(None, description="City of birth of the first person")
    nation1: str | None = Field(None, description="Country of birth of the first person")
    lng1: float | None = Field(None, description="Longitude of birth place of the first person")
    lat1: float | None = Field(None, description="Latitude of birth place of the first person")
    tz_str1: str | None = Field(None, description="Timezone string of the first person")
    
    name2: str = Field(..., description="Name of the second person")
    birth_date2: datetime = Field(..., description="Birth date and time of the second person")
    city2: str | None = Field(None, description="City of birth of the second person")
    nation2: str | None = Field(None, description="Country of birth of the second person")
    lng2: float | None = Field(None, description="Longitude of birth place of the second person")
    lat2: float | None = Field(None, description="Latitude of birth place of the second person")
    tz_str2: str | None = Field(None, description="Timezone string of the second person")
    
    houses_system: str | None = Field("P", description="House system identifier")

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
                "birth_date2": "1992-05-15T15:30:00",
                "city2": "Los Angeles",
                "nation2": "US",
                "lng2": -118.243,
                "lat2": 34.052,
                "tz_str2": "America/Los_Angeles",
                
                "houses_system": "P"
            }
        }
    }

# Report Response Schemas
class NatalReportResponse(BaseModel):
    """Schema for natal chart report response."""
    title: str = Field(..., description="Report title")
    data_table: str = Field(..., description="Table containing birth details")
    planets_table: str = Field(..., description="Table containing planet positions")
    houses_table: str = Field(..., description="Table containing house positions")
    full_report: str = Field(..., description="Complete report containing all tables")

class SynastryReportResponse(BaseModel):
    """Schema for synastry report response."""
    person1: Dict[str, str] = Field(..., description="Report data for the first person")
    person2: Dict[str, str] = Field(..., description="Report data for the second person")

# Schema for LLM Interpretation Request (placeholder for future implementation)
class InterpretationRequest(BaseModel):
    """Schema for chart interpretation request."""
    report_data: Dict[str, Any] = Field(..., description="Report data to be interpreted")
    interpretation_type: str = Field(..., description="Type of interpretation (e.g., 'natal', 'synastry')")
    aspects_focus: bool = Field(True, description="Whether to focus on aspects interpretation")
    houses_focus: bool = Field(True, description="Whether to focus on house placements interpretation")
    planets_focus: bool = Field(True, description="Whether to focus on planet interpretations")
    tone: str = Field("neutral", description="Tone of the interpretation (neutral, detailed, beginner-friendly)")
    max_length: int | None = Field(None, description="Maximum length of the interpretation in words")

    model_config = {
        "json_schema_extra": {
            "example": {
                "report_data": {
                    "title": "Kerykeion report for John Doe",
                    "planets_table": "...",
                    "houses_table": "...",
                    "data_table": "..."
                },
                "interpretation_type": "natal",
                "aspects_focus": True,
                "houses_focus": True,
                "planets_focus": True,
                "tone": "beginner-friendly",
                "max_length": 1000
            }
        }
    }

# Schema for LLM Interpretation Response (placeholder for future implementation)
class InterpretationResponse(BaseModel):
    """Schema for chart interpretation response."""
    interpretation: str = Field(..., description="Textual interpretation of the chart")
    highlights: list[str] = Field(default_factory=list, description="Key highlights of the interpretation")
    suggestions: list[str] = Field(default_factory=list, description="Suggestions based on the chart interpretation") 