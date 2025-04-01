"""Chart visualization API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from app.core.exceptions import ChartCalculationError, InvalidBirthDataError, LocationError
from app.core.config import Settings
from app.core.dependencies import get_settings
from app.schemas.chart_visualization import (
    NatalChartVisualizationRequest,
    NatalChartVisualizationResponse,
    SynastryChartVisualizationRequest,
    SynastryChartVisualizationResponse
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

@router.post("/natal", response_model=NatalChartVisualizationResponse)
async def generate_natal_chart_visualization(
    request: NatalChartVisualizationRequest,
    settings: Settings = Depends(get_settings)
) -> NatalChartVisualizationResponse:
    """
    Generate and save a natal chart visualization.
    
    Returns the chart ID and URL to access the SVG.
    """
    try:
        # Convert the birth_date from ISO format string to datetime
        try:
            birth_date = datetime.fromisoformat(request.birth_date)
        except ValueError:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid birth date format: {request.birth_date}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate the chart visualization
        result = ChartVisualizationService.generate_natal_chart_svg(
            name=request.name,
            birth_date=birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            chart_id=request.chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.dict() if request.config else None,
            settings=settings
        )
        
        return NatalChartVisualizationResponse(
            chart_id=result["chart_id"],
            svg_url=result["svg_url"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart: {str(e)}")

@router.post("/synastry", response_model=SynastryChartVisualizationResponse)
async def generate_synastry_chart_visualization(
    request: SynastryChartVisualizationRequest,
    settings: Settings = Depends(get_settings)
) -> SynastryChartVisualizationResponse:
    """
    Generate and save a synastry chart visualization comparing two natal charts.
    
    Returns the chart ID and URL to access the SVG.
    """
    try:
        # Convert the birth dates from ISO format strings to datetime
        try:
            birth_date1 = datetime.fromisoformat(request.birth_date1)
            birth_date2 = datetime.fromisoformat(request.birth_date2)
        except ValueError as e:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid birth date format: {str(e)}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate the synastry chart visualization
        result = ChartVisualizationService.generate_synastry_chart_svg(
            name1=request.name1,
            birth_date1=birth_date1,
            name2=request.name2,
            birth_date2=birth_date2,
            city1=request.city1,
            nation1=request.nation1,
            lng1=request.lng1,
            lat1=request.lat1,
            tz_str1=request.tz_str1,
            city2=request.city2,
            nation2=request.nation2,
            lng2=request.lng2,
            lat2=request.lat2,
            tz_str2=request.tz_str2,
            chart_id=request.chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.dict() if request.config else None,
            settings=settings
        )
        
        return SynastryChartVisualizationResponse(
            chart_id=result["chart_id"],
            svg_url=result["svg_url"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating synastry chart: {str(e)}") 