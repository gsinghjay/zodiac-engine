"""Synastry chart router module."""
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/synastry",
    tags=["synastry-chart"],
)

@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def calculate_synastry_chart():
    """Placeholder for synastry chart calculation endpoint."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Synastry chart calculation not yet implemented"
    ) 