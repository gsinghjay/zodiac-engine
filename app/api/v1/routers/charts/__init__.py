"""Charts router initialization."""
from fastapi import APIRouter

from app.api.v1.routers.charts.natal import router as natal_router
from app.api.v1.routers.charts.visualization import router as visualization_router
from app.api.v1.routers.charts.reports import router as reports_router
from app.api.v1.routers.charts.interpretations import router as interpretations_router

# Create the charts router
router = APIRouter(
    prefix="/charts",
    tags=["charts"]
)

# Include individual chart type routers
router.include_router(natal_router)
router.include_router(visualization_router)
router.include_router(reports_router)
router.include_router(interpretations_router)

# Export the router for use in the main API
__all__ = ["router"]
