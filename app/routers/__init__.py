"""Routers initialization."""
from fastapi import APIRouter

from app.routers.static import router as static_router

# Create the main router
router = APIRouter()

# Include static router
router.include_router(static_router)

# Export the router for use in the main app
__all__ = ["router"]
