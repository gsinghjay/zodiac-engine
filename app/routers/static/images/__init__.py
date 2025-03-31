"""Static images router initialization."""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.status import HTTP_404_NOT_FOUND

# Create the images router
router = APIRouter(
    prefix="/images",
    tags=["images"]
)

# Define the directory where SVG images will be stored
SVG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")

# Ensure the directory exists
os.makedirs(SVG_DIR, exist_ok=True)

@router.get(
    "/charts/{chart_id}",
    response_class=FileResponse,
    summary="Get Chart SVG",
    description="Retrieve an SVG visualization of a chart by its ID.",
    responses={
        404: {
            "description": "Chart not found",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 404,
                            "message": "Chart not found",
                            "type": "NotFoundError",
                            "path": "/static/images/charts/{chart_id}"
                        }
                    }
                }
            }
        }
    }
)
async def get_chart_svg(chart_id: str):
    """Get SVG visualization of a chart by ID."""
    svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
    
    if not os.path.exists(svg_path):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Chart with ID {chart_id} not found"
        )
    
    return FileResponse(svg_path)
