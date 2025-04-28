"""Natal chart router module."""
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.core.dependencies import AstrologyServiceDep
from app.core.exceptions import (
    ChartCalculationError,
    InvalidBirthDataError,
    LocationError
)
from app.schemas.natal_chart import NatalChartRequest, NatalChartResponse
from app.services.astrology import AstrologyService

router = APIRouter(
    prefix="/natal",
    tags=["natal-chart"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "examples": {
                        "InvalidBirthData": {
                            "summary": "Invalid birth data",
                            "value": {
                                "error": {
                                    "code": 400,
                                    "message": "Invalid birth data provided",
                                    "type": "InvalidBirthDataError",
                                    "path": "/api/v1/charts/natal/"
                                }
                            }
                        },
                        "InvalidLocation": {
                            "summary": "Invalid location",
                            "value": {
                                "error": {
                                    "code": 400,
                                    "message": "Invalid location coordinates",
                                    "type": "LocationError",
                                    "path": "/api/v1/charts/natal/"
                                }
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 500,
                            "message": "Error calculating astrological chart",
                            "type": "ChartCalculationError",
                            "path": "/api/v1/charts/natal/"
                        }
                    }
                }
            }
        }
    }
)

@router.post(
    "/",
    response_model=NatalChartResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    summary="Calculate Natal Chart",
    description="""
    Calculate a complete natal chart based on birth data.
    
    The natal chart includes:
    * Planetary positions and aspects
    * House cusps and placements
    * Zodiac sign positions
    * Retrograde status for applicable planets
    * Lunar Nodes (True/Mean)
    * Lilith (Mean)
    * Chiron
    * Complete aspect data with orbs
    * House system information
    
    You can provide either city/country or exact coordinates (longitude/latitude).
    If both are provided, coordinates take precedence.
    
    You can also specify which house system to use. The default is Placidus ('P').
    Other options include:
    - 'W': Whole Sign
    - 'K': Koch
    - 'R': Regiomontanus
    - 'C': Campanus
    - 'E': Equal (MC)
    - 'A': Equal (Ascendant)
    - 'T': Topocentric
    - 'O': Porphyry
    - 'B': Alcabitius
    - 'M': Morinus
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully calculated natal chart",
            "content": {
                "application/json": {
                    "example": {
                        "name": "John Doe",
                        "birth_date": "1990-01-01T12:00:00",
                        "planets": [
                            {
                                "name": "Sun",
                                "sign": "Capricorn",
                                "position": 10.5,
                                "house": 1,
                                "retrograde": False
                            }
                        ],
                        "houses": {
                            "1": 0.0,
                            "2": 30.0,
                            "3": 60.0
                        },
                        "aspects": [
                            {
                                "p1_name": "Sun",
                                "p2_name": "Moon",
                                "aspect": "trine",
                                "orbit": 120.0
                            }
                        ],
                        "house_system": {
                            "name": "Placidus",
                            "identifier": "P"
                        }
                    }
                }
            }
        }
    }
)
def calculate_natal_chart(
    request: NatalChartRequest,
    astrology_service: AstrologyServiceDep
) -> NatalChartResponse:
    """Calculate natal chart for given birth data."""
    try:
        # Validate birth data
        if not request.birth_date:
            raise InvalidBirthDataError("Birth date is required")
            
        # Validate location data
        if not (request.city and request.nation) and not (request.lng and request.lat):
            raise LocationError(
                "Either city/nation or longitude/latitude must be provided"
            )

        return astrology_service.calculate_natal_chart(
            name=request.name,
            birth_date=request.birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            houses_system=request.houses_system
        )
    except Exception as e:
        if isinstance(e, (InvalidBirthDataError, LocationError)):
            raise
        raise ChartCalculationError(str(e)) 