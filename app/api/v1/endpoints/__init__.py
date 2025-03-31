"""API v1 endpoints initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints.charts import router as charts_router

# Create the endpoints router
router = APIRouter()

# Include charts router
router.include_router(charts_router)

# Export the router for use in the main v1 router
__all__ = ["router"]
