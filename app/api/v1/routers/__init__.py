"""API v1 routers initialization."""
from fastapi import APIRouter

from app.api.v1.routers.charts import router as charts_router
from app.api.v1.routers.geo import router as geo_router

# Create the routers router
router = APIRouter()

# Include charts router
router.include_router(charts_router)

# Include geo router
router.include_router(geo_router)

# Export the router for use in the main v1 router
__all__ = ["router"]
