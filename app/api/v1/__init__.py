"""API v1 router initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints import router as endpoints_router

# Create the main v1 router with prefix and tag
router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

# Include endpoints router
router.include_router(endpoints_router)

# Export the router for use in the main API router
__all__ = ["router"]
