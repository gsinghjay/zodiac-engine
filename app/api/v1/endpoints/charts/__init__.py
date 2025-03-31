"""Charts router initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints.charts.natal import router as natal_router
from app.api.v1.endpoints.charts.visualization import router as visualization_router

# Create the charts router
router = APIRouter(
    prefix="/charts",
    tags=["charts"]
)

# Include individual chart type routers
router.include_router(natal_router)
router.include_router(visualization_router)

# Export the router for use in the main API
__all__ = ["router"]
