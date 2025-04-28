"""Transit chart router module."""
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/transit",
    tags=["transit-chart"],
)

@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def calculate_transit_chart():
    """Placeholder for transit chart calculation endpoint."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Transit chart calculation not yet implemented"
    ) 