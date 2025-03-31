"""Chart visualization API endpoints."""
from fastapi import APIRouter, HTTPException, Depends

from app.core.exceptions import ChartCalculationError, InvalidBirthDataError, LocationError
from app.schemas.chart_visualization import (
    NatalChartVisualizationRequest,
    ChartVisualizationResponse,
    SynastryChartVisualizationRequest
)
from app.services.chart_visualization import ChartVisualizationService

router = APIRouter(
    prefix="/visualization",
    tags=["chart-visualization"],
    responses={
        400: {
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
                                    "path": "/api/v1/charts/visualization/natal"
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
                                    "path": "/api/v1/charts/visualization/natal"
                                }
                            }
                        }
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 500,
                            "message": "Error generating chart visualization",
                            "type": "ChartCalculationError",
                            "path": "/api/v1/charts/visualization/natal"
                        }
                    }
                }
            }
        }
    }
)

@router.post(
    "/natal",
    response_model=ChartVisualizationResponse,
    summary="Generate Natal Chart Visualization",
    description="""
    Generate an SVG visualization of a natal chart and save it for later retrieval.
    
    The chart is generated using Kerykeion's visualization system and includes:
    * Zodiac wheel with houses and signs
    * Planet positions visualized on the wheel
    * Aspects between planets
    * Chart information and planetary positions
    
    You can provide either city/country or exact coordinates (longitude/latitude).
    If both are provided, coordinates take precedence.
    
    The resulting SVG can be accessed via the returned URL.
    Optionally provide a custom chart_id, otherwise a unique ID will be generated.
    """
)
async def generate_natal_chart_visualization(
    request: NatalChartVisualizationRequest
) -> ChartVisualizationResponse:
    """Generate an SVG visualization of a natal chart."""
    try:
        # Validate birth data
        if not request.birth_date:
            raise InvalidBirthDataError("Birth date is required")
            
        # Validate location data
        if not (request.city and request.nation) and not (request.lng and request.lat):
            raise LocationError(
                "Either city/nation or longitude/latitude must be provided"
            )
        
        # Generate the chart visualization
        result = ChartVisualizationService.generate_natal_chart_svg(
            name=request.name,
            birth_date=request.birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            houses_system=request.houses_system,
            theme=request.theme,
            chart_language=request.chart_language,
            chart_id=request.chart_id
        )
        
        # Return the response
        return ChartVisualizationResponse(
            chart_id=result["chart_id"],
            svg_url=result["svg_url"]
        )
    
    except Exception as e:
        if isinstance(e, (InvalidBirthDataError, LocationError)):
            raise
        raise ChartCalculationError(str(e))

@router.post(
    "/synastry",
    response_model=ChartVisualizationResponse,
    summary="Generate Synastry Chart Visualization",
    description="""
    Generate an SVG visualization of a synastry chart between two people and save it.
    
    The chart is generated using Kerykeion's visualization system and includes:
    * Combined chart wheel showing both people's planetary positions
    * Aspects between the planets of both individuals
    * Chart information and comparison details
    
    The resulting SVG can be accessed via the returned URL.
    Optionally provide a custom chart_id, otherwise a unique ID will be generated.
    """
)
async def generate_synastry_chart_visualization(
    request: SynastryChartVisualizationRequest
) -> ChartVisualizationResponse:
    """Generate an SVG visualization of a synastry chart."""
    try:
        # Validate first person birth data
        if not request.birth_date1:
            raise InvalidBirthDataError("Birth date for first person is required")
            
        # Validate second person birth data
        if not request.birth_date2:
            raise InvalidBirthDataError("Birth date for second person is required")
            
        # Validate first person location data
        if not (request.city1 and request.nation1) and not (request.lng1 and request.lat1):
            raise LocationError(
                "Either city/nation or longitude/latitude must be provided for first person"
            )
            
        # Validate second person location data
        if not (request.city2 and request.nation2) and not (request.lng2 and request.lat2):
            raise LocationError(
                "Either city/nation or longitude/latitude must be provided for second person"
            )
        
        # Generate the chart visualization
        result = ChartVisualizationService.generate_synastry_chart_svg(
            name1=request.name1,
            birth_date1=request.birth_date1,
            city1=request.city1,
            nation1=request.nation1,
            lng1=request.lng1,
            lat1=request.lat1,
            tz_str1=request.tz_str1,
            name2=request.name2,
            birth_date2=request.birth_date2,
            city2=request.city2,
            nation2=request.nation2,
            lng2=request.lng2,
            lat2=request.lat2,
            tz_str2=request.tz_str2,
            houses_system=request.houses_system,
            theme=request.theme,
            chart_language=request.chart_language,
            chart_id=request.chart_id
        )
        
        # Return the response
        return ChartVisualizationResponse(
            chart_id=result["chart_id"],
            svg_url=result["svg_url"]
        )
    
    except Exception as e:
        if isinstance(e, (InvalidBirthDataError, LocationError)):
            raise
        raise ChartCalculationError(str(e)) 