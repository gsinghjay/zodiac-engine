"""Web interface routes."""
import json
import uuid
import pytz
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, Dict, Any, List

from app.templates import templates
from app.core.config import settings
from app.core.dependencies import ChartVisualizationServiceDep
from app.services.chart_visualization import ChartVisualizationService
from app.schemas.chart_visualization import AspectConfiguration, ChartConfiguration

router = APIRouter(
    tags=["web"],
)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "version": settings.VERSION
        }
    )

@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "version": settings.VERSION
        }
    )

@router.post("/generate-chart", response_class=HTMLResponse)
async def generate_chart(
    request: Request,
    background_tasks: BackgroundTasks,
    chart_service: ChartVisualizationServiceDep,
    chart_type: str = Form(...),
    name: str = Form(...),
    birth_date: str = Form(...),
    city: str = Form(...),
    nation: str = Form(...),
    lng: Optional[float] = Form(None),
    lat: Optional[float] = Form(None),
    tz_str: Optional[str] = Form(None),
    houses_system: str = Form(...),
    theme: str = Form(...),
    language: str = Form(...),
    sidereal_mode: Optional[str] = Form(None),
):
    """Generate astrological chart based on form submission."""
    try:
        # Validate required fields
        missing_fields = []
        if lng is None:
            missing_fields.append("Longitude")
        if lat is None:
            missing_fields.append("Latitude")
        if not tz_str:
            missing_fields.append("Timezone")
            
        if missing_fields:
            raise HTTPException(
                status_code=422,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
            
        # Validate longitude and latitude
        if lng is not None and (lng < -180 or lng > 180):
            raise HTTPException(
                status_code=422,
                detail="Longitude must be between -180 and 180 degrees"
            )
            
        if lat is not None and (lat < -90 or lat > 90):
            raise HTTPException(
                status_code=422,
                detail="Latitude must be between -90 and 90 degrees"
            )
            
        # Validate timezone
        try:
            if tz_str:
                pytz.timezone(tz_str)
        except pytz.exceptions.UnknownTimeZoneError:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid timezone: {tz_str}. Please select a valid timezone."
            )
            
        # Convert the birth_date from form format to datetime
        try:
            birth_date_dt = datetime.fromisoformat(birth_date)
        except ValueError:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid birth date format: {birth_date}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate chart ID
        chart_id = f"{chart_type.lower()}_{uuid.uuid4().hex[:8]}"
        
        # Prepare chart configuration
        config = {
            "houses_system": houses_system,
            "zodiac_type": "Tropic" if chart_type.lower() == "western" else "Sidereal",
            "perspective_type": "Apparent Geocentric",
            "active_points": [
                "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
                "Uranus", "Neptune", "Pluto", "Ascendant", "Medium_Coeli", 
                "Descendant", "Imum_Coeli", "Mean_Node", "True_Node", 
                "Mean_South_Node", "True_South_Node", "Chiron", "Mean_Lilith"
            ],
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 7},
                {"name": "square", "orb": 7},
                {"name": "sextile", "orb": 6},
                {"name": "semi-sextile", "orb": 3},
                {"name": "semi-square", "orb": 3},
                {"name": "quincunx", "orb": 3},
            ]
        }
        
        # Add sidereal mode for Vedic charts
        if chart_type.lower() == "vedic" and sidereal_mode:
            config["sidereal_mode"] = sidereal_mode
            
        # Generate the chart in the background
        background_tasks.add_task(
            chart_service.generate_natal_chart_svg,
            name=name,
            birth_date=birth_date_dt,
            city=city,
            nation=nation,
            lng=lng,
            lat=lat,
            tz_str=tz_str,
            chart_id=chart_id,
            theme=theme,
            chart_language=language,
            config=config
        )
        
        # Return the template with the chart URL
        svg_url = f"/static/images/svg/{chart_id}.svg"
        
        return templates.TemplateResponse(
            "home.html", 
            {
                "request": request,
                "chart_url": svg_url,
                "version": settings.VERSION
            }
        )
        
    except HTTPException as e:
        # Return the specific error
        return templates.TemplateResponse(
            "home.html", 
            {
                "request": request,
                "error": e.detail,
                "version": settings.VERSION
            }
        )
    except Exception as e:
        # Handle other errors and return to the form with an error message
        return templates.TemplateResponse(
            "home.html", 
            {
                "request": request,
                "error": str(e),
                "version": settings.VERSION
            }
        ) 