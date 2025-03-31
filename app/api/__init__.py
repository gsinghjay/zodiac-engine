"""API router initialization."""
from fastapi import APIRouter

from app.api.v1 import router as v1_router

# Create the main API router
router = APIRouter()

# Include API version routers
router.include_router(v1_router)

# Export the router for use in the main app
__all__ = ["router"]
