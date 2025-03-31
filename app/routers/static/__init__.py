"""Static router initialization."""
from fastapi import APIRouter

from app.routers.static.images import router as images_router

# Create the static router
router = APIRouter(
    prefix="/static",
    tags=["static"]
)

# Include images router
router.include_router(images_router)

# Export the router for use in the main routers
__all__ = ["router"]
