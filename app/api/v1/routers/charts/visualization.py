"""Chart visualization API endpoints."""
from typing import Annotated
import uuid
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from datetime import datetime

from app.core.exceptions import ChartCalculationError, InvalidBirthDataError, LocationError
from app.core.dependencies import ChartVisualizationServiceDep
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
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
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
    response_model=NatalChartVisualizationResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate Natal Chart Visualization",
    description="""
    Generate and save a natal chart visualization.
    
    This endpoint accepts birth details and configuration options to create a custom chart.
    The SVG generation happens in the background, and the endpoint returns immediately with a chart ID.
    
    You can specify:
    - Theme: dark (default), light, classic, dark-high-contrast
    - Language: EN (default), ES, IT, FR, DE, etc.
    - Configuration options like house system, active points, and aspect orbs
    
    Returns a chart ID and URL to access the SVG once it's generated.
    """
)
async def generate_natal_chart_visualization(
    request: NatalChartVisualizationRequest,
    background_tasks: BackgroundTasks,
    chart_service: ChartVisualizationServiceDep
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
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"Invalid birth date format: {request.birth_date}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate a unique chart_id if not provided
        chart_id = request.chart_id or f"natal_{uuid.uuid4().hex[:8]}"
        
        # Create a placeholder URL that will be valid once the background task completes
        svg_url = f"/static/images/svg/{chart_id}.svg"
        
        # Schedule the chart generation as a background task
        background_tasks.add_task(
            chart_service.generate_natal_chart_svg,
            name=request.name,
            birth_date=birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            chart_id=chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.model_dump() if request.config else None
        )
        
        # Return the response immediately
        return NatalChartVisualizationResponse(
            chart_id=chart_id,
            svg_url=svg_url
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error generating chart: {str(e)}"
        )

@router.post(
    "/synastry", 
    response_model=SynastryChartVisualizationResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate Synastry Chart Visualization",
    description="""
    Generate and save a synastry chart visualization comparing two natal charts.
    
    This endpoint accepts birth details for two individuals and configuration options to create a custom synastry chart.
    The SVG generation happens in the background, and the endpoint returns immediately with a chart ID.
    
    You can specify:
    - Theme: dark (default), light, classic, dark-high-contrast
    - Language: EN (default), ES, IT, FR, DE, etc.
    - Configuration options like house system, active points, and aspect orbs
    
    Returns a chart ID and URL to access the SVG once it's generated.
    """
)
async def generate_synastry_chart_visualization(
    request: SynastryChartVisualizationRequest,
    background_tasks: BackgroundTasks,
    chart_service: ChartVisualizationServiceDep
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
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"Invalid birth date format: {str(e)}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate a unique chart_id if not provided
        chart_id = request.chart_id or f"synastry_{uuid.uuid4().hex[:8]}"
        
        # Create a placeholder URL that will be valid once the background task completes
        svg_url = f"/static/images/svg/{chart_id}.svg"
        
        # Schedule the chart generation as a background task
        background_tasks.add_task(
            chart_service.generate_synastry_chart_svg,
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
            chart_id=chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.model_dump() if request.config else None
        )
        
        # Return the response immediately
        return SynastryChartVisualizationResponse(
            chart_id=chart_id,
            svg_url=svg_url
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error generating synastry chart: {str(e)}"
        ) 