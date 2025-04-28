"""Dependency functions for FastAPI."""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.services.astrology import AstrologyService
from app.services.chart_visualization import ChartVisualizationService

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get application settings as a dependency.
    
    Uses lru_cache for caching to avoid reloading settings on every request.
    """
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]

def get_astrology_service() -> AstrologyService:
    """
    Get an instance of the AstrologyService.
    
    This dependency can be used in route functions to get access to astrology-related operations.
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