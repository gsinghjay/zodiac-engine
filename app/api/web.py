"""Web interface routes."""
import json
import uuid
import pytz
import os
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, BackgroundTasks, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from typing import Optional, Dict, Any, List, Union
from pathlib import Path

from app.templates import templates
from app.core.config import settings
from app.core.dependencies import ChartVisualizationServiceDep, GeoServiceDep
from app.services.chart_visualization import ChartVisualizationService
from app.services.geo_service import GeoService
from app.schemas.chart_visualization import AspectConfiguration, ChartConfiguration

router = APIRouter(
    tags=["web"],
)

# Create a dictionary to temporarily store chart data
# In a production app, you would use a database
chart_cache = {}

@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "version": settings.VERSION
        }
    )

@router.get("/home", response_class=HTMLResponse, name="home_page")
async def home_page(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "version": settings.VERSION
        }
    )

@router.get("/chart/{chart_id}", response_class=HTMLResponse, name="chart_details")
async def chart_details(request: Request, chart_id: str):
    """Render the chart details page."""
    # Get chart data from cache or storage
    chart_data = chart_cache.get(chart_id)
    
    if not chart_data:
        # If chart data is not found, redirect to home
        return RedirectResponse(url="/home", status_code=303)
    
    # Chart URL
    chart_url = f"/static/images/svg/{chart_id}.svg"
    
    # Return the template with chart details
    return templates.TemplateResponse(
        "chart_details.html", 
        {
            "request": request,
            "chart_url": chart_url,
            "chart_data": chart_data,
            "chart_id": chart_id,
            "version": settings.VERSION
        }
    )

@router.get("/download-chart/{chart_id}", name="download_chart")
async def download_chart(chart_id: str, format: str = "svg"):
    """Download chart in various formats."""
    # Base file path for the SVG
    svg_path = Path(f"app/static/images/svg/{chart_id}.svg")
    
    # Check if the file exists
    if not svg_path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    
    # Return appropriate file based on format
    if format.lower() == "svg":
        return FileResponse(
            svg_path, 
            media_type="image/svg+xml",
            filename=f"astrological_chart_{chart_id}.svg"
        )
    elif format.lower() == "png":
        # In a real app, you would convert SVG to PNG here
        # For now, we'll just return the SVG
        return FileResponse(
            svg_path, 
            media_type="image/svg+xml",
            filename=f"astrological_chart_{chart_id}.svg"
        )
    elif format.lower() == "pdf":
        # In a real app, you would convert SVG to PDF here
        # For now, we'll just return the SVG
        return FileResponse(
            svg_path, 
            media_type="image/svg+xml",
            filename=f"astrological_chart_{chart_id}.svg"
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

@router.post("/search-location", response_class=HTMLResponse, name="search_location")
async def search_location(
    request: Request,
    geo_service: GeoServiceDep,
    city: Optional[str] = Form(None),
    hx_request: Optional[str] = Header(None)
):
    """Search for locations based on city name."""
    try:
        if not city or len(city.strip()) < 2:
            return templates.TemplateResponse(
                "fragments/location_results.html",
                {
                    "request": request,
                    "locations": [],
                    "error": "Please enter at least 2 characters for city search"
                }
            )
            
        # Search for locations using GeoService
        locations = await geo_service.search_cities(city)
        
        # For debugging
        print(f"Search results for '{city}': {len(locations)} locations found")
        
        # Return the locations fragment
        return templates.TemplateResponse(
            "fragments/location_results.html",
            {
                "request": request,
                "locations": locations
            }
        )
    except Exception as e:
        # For debugging
        print(f"Error in search_location: {str(e)}")
        
        return templates.TemplateResponse(
            "fragments/location_results.html",
            {
                "request": request,
                "locations": [],
                "error": str(e)
            }
        )

@router.post("/select-location", response_class=HTMLResponse, name="select_location")
async def select_location(
    request: Request,
    city: str = Form(...),
    nation: str = Form(...),
    lng: float = Form(...),
    lat: float = Form(...),
    tz_str: str = Form(...),
    hx_request: Optional[str] = Header(None)
):
    """Handle location selection and populate form fields."""
    print(f"Location selected: {city}, {nation}, lng: {lng}, lat: {lat}, tz: {tz_str}")
    
    return templates.TemplateResponse(
        "fragments/location_fields.html",
        {
            "request": request,
            "city": city,
            "nation": nation,
            "lng": lng,
            "lat": lat,
            "tz_str": tz_str
        }
    )

@router.post("/validate-form", response_class=HTMLResponse, name="validate_form")
async def validate_form(
    request: Request,
    name: Optional[str] = Form(None),
    birth_date: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    nation: Optional[str] = Form(None),
    lng: Optional[float] = Form(None),
    lat: Optional[float] = Form(None),
    tz_str: Optional[str] = Form(None),
    houses_system: Optional[str] = Form(None),
    hx_request: Optional[str] = Header(None)
):
    """Validate form data without generating a chart."""
    errors = []
    
    # Validate required fields
    if not name:
        errors.append("Name is required")
    
    # Validate birth date
    try:
        if birth_date:
            datetime.fromisoformat(birth_date)
        else:
            errors.append("Birth date is required")
    except ValueError:
        errors.append("Invalid birth date format")
    
    # Validate city/nation
    if not city:
        errors.append("City is required")
    if not nation:
        errors.append("Country is required")
    
    # Validate coordinates
    if lng is None:
        errors.append("Longitude is required")
    elif lng < -180 or lng > 180:
        errors.append("Longitude must be between -180 and 180 degrees")
        
    if lat is None:
        errors.append("Latitude is required")
    elif lat < -90 or lat > 90:
        errors.append("Latitude must be between -90 and 90 degrees")
    
    # Validate timezone
    if not tz_str:
        errors.append("Timezone is required")
    else:
        try:
            pytz.timezone(tz_str)
        except pytz.exceptions.UnknownTimeZoneError:
            errors.append(f"Invalid timezone: {tz_str}")
    
    # Return validation results
    return templates.TemplateResponse(
        "fragments/form_validation.html",
        {
            "request": request,
            "errors": errors
        }
    )

@router.post("/generate-chart", name="generate_chart")
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
    hx_request: Optional[str] = Header(None)
):
    """
    Generate astrological chart based on form submission and redirect to chart details page.
    
    Accepts house system names in human-readable format (e.g., "Whole Sign", "Placidus").
    These are mapped to the appropriate single-letter codes used by the Kerykeion library.
    
    Language codes (e.g., "en", "fr") are automatically converted to uppercase as required
    by the Kerykeion library.
    """
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
            birth_date_formatted = birth_date_dt.strftime("%B %d, %Y at %I:%M %p")
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
        
        # Store chart data in cache
        chart_cache[chart_id] = {
            "name": name,
            "birth_date": birth_date_formatted,
            "city": city,
            "nation": nation,
            "lat": lat,
            "lng": lng,
            "houses_system": houses_system,
            "chart_type": chart_type,
            "theme": theme,
            "language": language
        }
        
        # If HTMX request, return a redirect instruction
        if hx_request:
            return HTMLResponse(
                headers={
                    "HX-Redirect": f"/chart/{chart_id}"
                },
                content=""
            )
        
        # If regular form submission, redirect to chart details page
        return RedirectResponse(url=f"/chart/{chart_id}", status_code=303)
        
    except HTTPException as e:
        # Return the specific error
        if hx_request:
            return templates.TemplateResponse(
                "fragments/form_validation.html", 
                {
                    "request": request,
                    "errors": [e.detail]
                }
            )
        
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
        if hx_request:
            return templates.TemplateResponse(
                "fragments/form_validation.html", 
                {
                    "request": request,
                    "errors": [str(e)]
                }
            )
        
        return templates.TemplateResponse(
            "home.html", 
            {
                "request": request,
                "error": str(e),
                "version": settings.VERSION
            }
        ) 