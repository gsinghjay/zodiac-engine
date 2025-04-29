"""Routers initialization."""
from fastapi import APIRouter

from app.routers.web import router as web_router

# Create the main router
router = APIRouter()

# Include routers
router.include_router(web_router)

# Export the router for use in the main app
__all__ = ["router"]
