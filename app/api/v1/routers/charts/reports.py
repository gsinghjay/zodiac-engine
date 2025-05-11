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

        # Get birth place information
        birth_place = f"{request.city}, {request.nation}" if request.city and request.nation else "Unknown"

        # Generate report
        report_data = report_service.generate_natal_report(
            name=request.name,
            birth_date=request.birth_date,
            birth_place=birth_place,
            lat=request.lat or 0.0,
            lng=request.lng or 0.0,
            house_system=request.houses_system,
            timezone=request.tz_str
        )
        
        # The service now returns a dictionary with the correct structure for NatalReportResponse
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

        # Get birth place information
        birth_place1 = f"{request.city1}, {request.nation1}" if request.city1 and request.nation1 else "Unknown"
        birth_place2 = f"{request.city2}, {request.nation2}" if request.city2 and request.nation2 else "Unknown"

        # Generate report
        report_data = report_service.generate_synastry_report(
            person1_name=request.name1,
            person1_birth_date=request.birth_date1,
            person1_birth_place=birth_place1,
            person1_lat=request.lat1 or 0.0,
            person1_lng=request.lng1 or 0.0,
            person2_name=request.name2,
            person2_birth_date=request.birth_date2,
            person2_birth_place=birth_place2,
            person2_lat=request.lat2 or 0.0,
            person2_lng=request.lng2 or 0.0,
            house_system=request.houses_system,
            timezone=request.tz_str1 or request.tz_str2
        )
        
        # The service now returns a dictionary with the correct structure for SynastryReportResponse
        return SynastryReportResponse(**report_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating synastry report: {str(e)}"
        ) 