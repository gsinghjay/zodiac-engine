"""Dependency functions for FastAPI."""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.services.astrology import AstrologyService
from app.services.chart_visualization import ChartVisualizationService
from app.services.file_conversion import FileConversionService
from app.services.geo_service import GeoService
from app.services.report import ReportService
from app.services.interpretation import InterpretationService

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get application settings as a dependency.
    
    Uses lru_cache for caching to avoid reloading settings on every request.
    """
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]

@lru_cache(maxsize=32)
def get_astrology_service() -> AstrologyService:
    """
    Get an instance of the AstrologyService.
    
    This dependency can be used in route functions to get access to astrology-related operations.
    Uses lru_cache to reuse the service instance, improving performance.
    """
    return AstrologyService()

AstrologyServiceDep = Annotated[AstrologyService, Depends(get_astrology_service)]

def get_chart_visualization_service(settings: SettingsDep) -> ChartVisualizationService:
    """
    Get an instance of the ChartVisualizationService.
    
    This dependency requires settings and can be used in route functions
    to get access to chart visualization operations.
    """
    return ChartVisualizationService(settings=settings)

ChartVisualizationServiceDep = Annotated[ChartVisualizationService, Depends(get_chart_visualization_service)]

def get_geo_service(settings: SettingsDep) -> GeoService:
    """
    Get an instance of the GeoService.
    
    This dependency requires settings and can be used in route functions
    to get access to geolocation operations.
    """
    return GeoService(settings=settings)

GeoServiceDep = Annotated[GeoService, Depends(get_geo_service)]

@lru_cache(maxsize=32)
def get_file_conversion_service() -> FileConversionService:
    """
    Get an instance of the FileConversionService.
    
    This dependency can be used in route functions to get access to file conversion operations.
    Uses lru_cache to reuse the service instance, improving performance.
    """
    return FileConversionService()

FileConversionServiceDep = Annotated[FileConversionService, Depends(get_file_conversion_service)]

@lru_cache(maxsize=32)
def get_report_service() -> ReportService:
    """
    Get an instance of the ReportService.
    
    This dependency can be used in route functions to get access to report generation operations.
    Uses lru_cache to reuse the service instance, improving performance.
    """
    return ReportService()

ReportServiceDep = Annotated[ReportService, Depends(get_report_service)]

def get_interpretation_service(settings: SettingsDep) -> InterpretationService:
    """
    Get an instance of the InterpretationService.
    
    This dependency requires settings for LLM API keys and configuration.
    It can be used in route functions to get access to chart interpretation operations.
    """
    # Get API keys from settings
    llm_api_key = settings.LLM_API_KEY
    model_name = settings.LLM_MODEL_NAME or "gpt-4"
    
    return InterpretationService(llm_api_key=llm_api_key, model_name=model_name)

InterpretationServiceDep = Annotated[InterpretationService, Depends(get_interpretation_service)] 