"""Charts API endpoints initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints.charts import natal, transit, synastry, composite

# Create the charts router with prefix and tag
router = APIRouter(
    prefix="/charts",
    tags=["charts"]
)

# Include sub-routers
router.include_router(natal.router)
router.include_router(transit.router)
router.include_router(synastry.router)
router.include_router(composite.router)

# Export the router for use in the endpoints router
__all__ = ["router"]
