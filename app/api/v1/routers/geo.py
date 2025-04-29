"""Geolocation API routes."""
from typing import List

from fastapi import APIRouter, Query, HTTPException, Depends

from app.core.dependencies import GeoServiceDep
from app.services.geo_service import GeoLocation

router = APIRouter(
    prefix="/geo",
    tags=["geo"],
    responses={
        404: {"description": "Not found"},
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 500,
                            "message": "Internal server error",
                            "type": "ServerError"
                        }
                    }
                }
            }
        }
    }
)


@router.get(
    "/search",
    response_model=List[GeoLocation],
    summary="Search cities",
    description="Search for cities matching the query string.",
    responses={
        200: {
            "description": "List of matched locations with coordinates and timezone",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "New York",
                            "country_code": "US",
                            "latitude": 40.7128,
                            "longitude": -74.006,
                            "timezone": "America/New_York"
                        }
                    ]
                }
            }
        },
        400: {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 400,
                            "message": "Query parameter is required",
                            "type": "ValidationError"
                        }
                    }
                }
            }
        }
    }
)
async def search_cities(
    geo_service: GeoServiceDep,
    q: str = Query(..., description="Search query for city name"),
    max_rows: int = Query(10, description="Maximum number of results to return", ge=1, le=20)
) -> List[GeoLocation]:
    """
    Search for cities matching the query string.
    
    Args:
        geo_service: Injected geo service
        q: Search query for city name
        max_rows: Maximum number of results to return (default: 10, max: 20)
        
    Returns:
        List of matched locations with coordinates and timezone
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": 400,
                    "message": "Query must be at least 2 characters",
                    "type": "ValidationError"
                }
            }
        )
    
    results = geo_service.search_cities(q, max_rows)
    return results 