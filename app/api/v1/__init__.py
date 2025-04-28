"""API v1 router initialization."""
from fastapi import APIRouter

from app.api.v1.routers import router as routers_router

# Create the main v1 router with prefix and tag
router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

# Include endpoints router
router.include_router(routers_router)

# Export the router for use in the main API router
__all__ = ["router"]
