"""API router initialization."""
from fastapi import APIRouter

from app.api.v1 import router as v1_router
from app.api.web import router as web_router

# Create the main API router
router = APIRouter()

# Include API version routers
router.include_router(v1_router)

# Include web interface router
router.include_router(web_router)

# Export the router for use in the main app
__all__ = ["router"]
