"""Report generation router module."""
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.core.dependencies import ReportServiceDep
from app.schemas.report import (
    NatalReportRequest, 
    NatalReportResponse,
    SynastryReportRequest,
    SynastryReportResponse
)
from app.services.report import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["chart-reports"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 400,
                            "message": "Invalid birth data provided",
                            "type": "InvalidBirthDataError",
                            "path": "/api/v1/charts/reports/natal/"
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
                            "message": "Error generating report",
                            "type": "ReportGenerationError",
                            "path": "/api/v1/charts/reports/natal/"
                        }
                    }
                }
            }
        }
    }
)

@router.post(
    "/natal",
    response_model=NatalReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Natal Chart Report",
    description="""
    Generate a tabular report for a natal chart.
    
    This endpoint accepts birth details and returns a formatted report with tables for:
    - Birth data information
    - Planet positions, signs, and house placements
    - House cusp positions and signs
    
    The report is formatted as plain text tables that can be easily displayed
    or used as input for LLM-based interpretations.
    
    You can provide either city/country or exact coordinates (longitude/latitude).
    If both are provided, coordinates take precedence.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully generated natal chart report",
            "content": {
                "application/json": {
                    "example": {
                        "title": "+- Kerykeion report for John Doe -+",
                        "data_table": "ASCII table with birth data",
                        "planets_table": "ASCII table with planet positions",
                        "houses_table": "ASCII table with house positions",
                        "full_report": "Combined report with all tables"
                    }
                }
            }
        }
    }
)
def generate_natal_report(
    request: NatalReportRequest,
    report_service: ReportServiceDep
) -> NatalReportResponse:
    """Generate a report for a natal chart."""
    try:
        # Validate birth data
        if not request.birth_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Birth date is required"
            )
            
        # Validate location data
        if not (request.city and request.nation) and not (request.lng and request.lat):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either city/nation or longitude/latitude must be provided"
            )

        report_data = report_service.generate_natal_report(
            name=request.name,
            birth_date=request.birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            houses_system=request.houses_system
        )
        
        return NatalReportResponse(**report_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

@router.post(
    "/synastry",
    response_model=SynastryReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Synastry Report",
    description="""
    Generate tabular reports for two charts in a synastry comparison.
    
    This endpoint accepts birth details for two individuals and returns
    formatted reports for both charts with tables for:
    - Birth data information for both individuals
    - Planet positions, signs, and house placements for both charts
    - House cusp positions and signs for both charts
    
    The reports are formatted as plain text tables that can be easily displayed
    or used as input for LLM-based relationship interpretations.
    
    You must provide location information (either city/country or coordinates)
    for both individuals.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully generated synastry report",
            "content": {
                "application/json": {
                    "example": {
                        "person1": {
                            "title": "+- Kerykeion report for John Doe -+",
                            "data_table": "ASCII table with birth data",
                            "planets_table": "ASCII table with planet positions",
                            "houses_table": "ASCII table with house positions"
                        },
                        "person2": {
                            "title": "+- Kerykeion report for Jane Smith -+",
                            "data_table": "ASCII table with birth data",
                            "planets_table": "ASCII table with planet positions",
                            "houses_table": "ASCII table with house positions"
                        }
                    }
                }
            }
        }
    }
)
def generate_synastry_report(
    request: SynastryReportRequest,
    report_service: ReportServiceDep
) -> SynastryReportResponse:
    """Generate reports for two charts in a synastry comparison."""
    try:
        # Validate birth data for both individuals
        if not request.birth_date1 or not request.birth_date2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Birth dates are required for both individuals"
            )
            
        # Validate location data for first individual
        if not (request.city1 and request.nation1) and not (request.lng1 and request.lat1):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either city/nation or longitude/latitude must be provided for the first individual"
            )
            
        # Validate location data for second individual
        if not (request.city2 and request.nation2) and not (request.lng2 and request.lat2):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either city/nation or longitude/latitude must be provided for the second individual"
            )

        report_data = report_service.generate_synastry_report(
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
            
            houses_system=request.houses_system
        )
        
        return SynastryReportResponse(**report_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating synastry report: {str(e)}"
        ) 