"""Chart interpretation router module."""
from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import ValidationError

from app.core.dependencies import ReportServiceDep, InterpretationServiceDep
from app.schemas.report import InterpretationRequest, InterpretationResponse, NatalReportData, SynastryReportData
from app.services.report import ReportService
from app.services.interpretation import InterpretationService

router = APIRouter(
    prefix="/interpretations",
    tags=["chart-interpretations"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 400,
                            "message": "Invalid chart data",
                            "type": "InvalidChartDataError",
                            "path": "/api/v1/charts/interpretations/natal/"
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
                            "message": "Error generating interpretation",
                            "type": "InterpretationError",
                            "path": "/api/v1/charts/interpretations/natal/"
                        }
                    }
                }
            }
        }
    }
)

@router.post(
    "/natal",
    response_model=InterpretationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Natal Chart Interpretation",
    description="""
    Generate an interpretation of a natal chart using LLM.
    
    This endpoint accepts natal chart report data and interpretation preferences,
    and returns a detailed textual interpretation of the chart.
    
    You can customize the interpretation by specifying focus areas (planets, houses, aspects),
    the tone (beginner-friendly, neutral, detailed), and maximum length.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully generated chart interpretation",
            "content": {
                "application/json": {
                    "example": {
                        "interpretation": "This is an interpretation of the natal chart...",
                        "highlights": ["Strong Mars in the 10th house indicates leadership abilities", 
                                      "Moon-Venus trine suggests emotional warmth"],
                        "suggestions": ["Focus on developing leadership skills", 
                                       "Creative pursuits may bring emotional fulfillment"]
                    }
                }
            }
        }
    }
)
def generate_natal_interpretation(
    request: InterpretationRequest,
    interpretation_service: InterpretationServiceDep
) -> InterpretationResponse:
    """Generate an interpretation for a natal chart."""
    try:
        if not request.report_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Report data is required for interpretation"
            )
            
        if request.interpretation_type != "natal":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid interpretation type. Must be 'natal' for this endpoint."
            )
            
        # Validate that the report data is the correct type for natal interpretation
        if not isinstance(request.report_data, NatalReportData):
            try:
                # Attempt to convert to NatalReportData if it's in the right format
                natal_report_data = NatalReportData.model_validate(request.report_data)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid report data format for natal chart interpretation: {str(e)}"
                )
        else:
            natal_report_data = request.report_data

        interpretation_result = interpretation_service.interpret_natal_chart(
            report_data=natal_report_data,
            aspects_focus=request.aspects_focus,
            houses_focus=request.houses_focus,
            planets_focus=request.planets_focus,
            tone=request.tone,
            max_length=request.max_length
        )
        
        return InterpretationResponse(**interpretation_result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating interpretation: {str(e)}"
        )

@router.post(
    "/synastry",
    response_model=InterpretationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Synastry Chart Interpretation",
    description="""
    Generate an interpretation of a synastry chart comparison using LLM.
    
    This endpoint accepts synastry chart report data and interpretation preferences,
    and returns a detailed textual interpretation of the relationship dynamics.
    
    You can customize the interpretation by specifying focus areas (aspects, compatibility),
    the tone (beginner-friendly, neutral, detailed), and maximum length.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully generated synastry interpretation",
            "content": {
                "application/json": {
                    "example": {
                        "interpretation": "This is an interpretation of the relationship dynamics...",
                        "highlights": ["Strong Venus-Mars connection indicates physical attraction", 
                                      "Moon-Moon square suggests emotional challenges"],
                        "suggestions": ["Focus on communication to address emotional differences", 
                                       "Physical activities together may strengthen your bond"]
                    }
                }
            }
        }
    }
)
def generate_synastry_interpretation(
    request: InterpretationRequest,
    interpretation_service: InterpretationServiceDep
) -> InterpretationResponse:
    """Generate an interpretation for a synastry chart comparison."""
    try:
        if not request.report_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Report data is required for interpretation"
            )
            
        if request.interpretation_type != "synastry":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid interpretation type. Must be 'synastry' for this endpoint."
            )
            
        # Validate that the report data is the correct type for synastry interpretation
        if not isinstance(request.report_data, SynastryReportData):
            try:
                # Attempt to convert to SynastryReportData if it's in the right format
                synastry_report_data = SynastryReportData.model_validate(request.report_data)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid report data format for synastry chart interpretation: {str(e)}"
                )
        else:
            synastry_report_data = request.report_data

        interpretation_result = interpretation_service.interpret_synastry_chart(
            report_data=synastry_report_data,
            aspects_focus=request.aspects_focus,
            compatibility_focus=request.compatibility_focus,
            tone=request.tone,
            max_length=request.max_length
        )
        
        return InterpretationResponse(**interpretation_result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating synastry interpretation: {str(e)}"
        ) 