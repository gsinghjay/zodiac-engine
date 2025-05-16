"""Web interface routes."""
import json
import uuid
import pytz
import os
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, BackgroundTasks, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, Response
from typing import Optional, Dict, Any, List, Union, Literal
from pathlib import Path
import logging
from starlette.concurrency import run_in_threadpool

from app.templates import templates
from app.core.config import settings
from app.core.dependencies import (
    ChartVisualizationServiceDep, 
    GeoServiceDep, 
    FileConversionServiceDep,
    ReportServiceDep,
    InterpretationServiceDep
)
from app.services.chart_visualization import ChartVisualizationService
from app.services.geo_service import GeoService
from app.services.file_conversion import FileConversionService, OutputFormat
from app.services.report import ReportService
from app.services.interpretation import InterpretationService
from app.core.exceptions import FileConversionError
from app.schemas.chart_visualization import AspectConfiguration, ChartConfiguration
from app.schemas.report import NatalReportData

router = APIRouter(
    tags=["web"],
)

# Create a dictionary to temporarily store chart data
# In a production app, you would use a database
chart_cache = {}

logger = logging.getLogger(__name__)

def parse_birth_date_from_cache(birth_date_str: str) -> datetime:
    """
    Convert a formatted birth date string from the chart cache to a datetime object.
    
    Args:
        birth_date_str: Formatted date string (e.g., "July 17, 1994 at 10:30 AM")
        
    Returns:
        datetime: Parsed datetime object
    """
    try:
        # Try to directly parse the formatted date string
        # Example: "July 17, 1994 at 10:30 AM"
        return datetime.strptime(birth_date_str, "%B %d, %Y at %I:%M %p")
    except ValueError as e:
        logger.warning(f"Failed to parse birth_date with standard format: {e}")
        try:
            # Fallback for potential ISO format (YYYY-MM-DDTHH:MM:SS)
            return datetime.fromisoformat(birth_date_str)
        except ValueError:
            logger.error(f"Could not parse birth_date string: {birth_date_str}")
            # Return current time as a last resort to avoid breaking the entire application
            # This is not ideal, but better than crashing
            return datetime.now()

@router.get("/", response_class=HTMLResponse, name="landing")
async def landing(request: Request):
    """Render the landing page."""
    return templates.TemplateResponse(
        "landing.html", 
        {
            "request": request,
            "version": settings.VERSION
        }
    )

@router.get("/home", response_class=HTMLResponse, name="home_page")
@router.get("/chart-generator", response_class=HTMLResponse, name="chart_generator")
async def chart_generator(request: Request):
    """Render the chart generation page."""
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
async def download_chart(
    chart_id: str, 
    conversion_service: FileConversionServiceDep,
    format: Literal["svg", "png", "pdf", "jpg"] = "svg",
    dpi: int = 96
):
    """
    Download chart in various formats.
    
    Args:
        chart_id: The unique identifier for the chart
        conversion_service: FileConversionService dependency
        format: The desired output format (svg, png, pdf, jpg)
        dpi: The resolution in dots per inch for raster formats (png, jpg)
        
    Returns:
        The chart file in the requested format
    """
    # Base file path for the SVG
    svg_path = Path(f"app/static/images/svg/{chart_id}.svg")
    
    # Check if the file exists
    if not svg_path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    
    # Conversion logic based on format
    try:
        if format == "svg":
            # SVG doesn't need conversion, just return the file
            return FileResponse(
                svg_path,
                media_type="image/svg+xml",
                filename=f"{chart_id}.svg"
            )
        
        # For other formats, use the conversion service
        output_format = OutputFormat(format.upper())
        
        # Convert file
        result_path, content_type = conversion_service.convert_svg_file(
            svg_path, 
            output_format=output_format,
            dpi=dpi
        )
        
        # Set the proper filename extension
        extension = format.lower()
        
        # Return the converted file
        return FileResponse(
            result_path,
            media_type=content_type,
            filename=f"{chart_id}.{extension}"
        )
        
    except FileConversionError as e:
        logger.error(f"File conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error converting chart: {str(e)}")
    except Exception as e:
        logger.error(f"Error in download_chart: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chart: {str(e)}")

@router.get("/chart-report/{chart_id}", response_class=HTMLResponse, name="chart_report")
async def chart_report(
    request: Request,
    chart_id: str,
    report_service: ReportServiceDep,
    hx_request: Optional[str] = Header(None)
):
    """
    Generate and display a report for a chart.
    
    Args:
        request: The FastAPI request object
        chart_id: The unique identifier for the chart
        report_service: ReportService dependency
        hx_request: HTMX request header
        
    Returns:
        HTML template with the chart report
    """
    try:
        # Get chart data from cache
        if chart_id not in chart_cache:
            raise HTTPException(status_code=404, detail="Chart not found")
        
        chart_data = chart_cache[chart_id]
        
        # Convert birth_date string to datetime
        birth_date_dt = parse_birth_date_from_cache(chart_data["birth_date"])
        
        # Get birth place information
        birth_place = f"{chart_data['city']}, {chart_data['nation']}"
        
        # Generate report using ReportService
        report_data = report_service.generate_natal_report(
            name=chart_data["name"],
            birth_date=birth_date_dt,
            birth_place=birth_place,
            lat=chart_data["lat"],
            lng=chart_data["lng"],
            house_system=chart_data.get("houses_system", "Placidus"),
            timezone=chart_data.get("tz_str")
        )
        
        # Check if there's a note about Whole Sign houses in the full report
        has_whole_sign_note = "Note: For Whole Sign houses" in report_data["full_report"]
        whole_sign_note = "Note: For Whole Sign houses, all house positions are 0.0 as each house starts at 0° of its sign." if has_whole_sign_note else ""
        
        # Return the report fragment with structured data
        return templates.TemplateResponse(
            "fragments/report.html",
            {
                "request": request,
                "title": report_data["title"],
                "data_table": report_data["data_table"],
                "planets_table": report_data["planets_table"],
                "houses_table": report_data["houses_table"],
                "whole_sign_note": whole_sign_note
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return templates.TemplateResponse(
            "fragments/report.html",
            {
                "request": request,
                "error": f"Error generating report: {str(e)}"
            }
        )

@router.get("/interpret-chart/{chart_id}", response_class=HTMLResponse, name="interpret_chart")
async def interpret_chart(
    request: Request,
    chart_id: str,
    interpretation_service: InterpretationServiceDep,
    report_service: ReportServiceDep,
    planets_focus: bool = True,
    houses_focus: bool = True,
    aspects_focus: bool = True,
    tone: Literal["beginner-friendly", "neutral", "detailed"] = "neutral",
    max_length: int = 1000,
    hx_request: Optional[str] = Header(None)
):
    """
    Generate and display an interpretation for a chart.
    
    Args:
        request: The FastAPI request object
        chart_id: The unique identifier for the chart
        interpretation_service: InterpretationService dependency
        report_service: ReportService dependency
        planets_focus: Whether to focus on planet interpretations
        houses_focus: Whether to focus on house placement interpretations
        aspects_focus: Whether to focus on aspect interpretations
        tone: The tone of the interpretation
        max_length: Maximum length of the interpretation in words
        hx_request: HTMX request header
        
    Returns:
        HTML template with the chart interpretation
    """
    try:
        # Get chart data from cache
        if chart_id not in chart_cache:
            raise HTTPException(status_code=404, detail="Chart not found")
        
        chart_data = chart_cache[chart_id]
        
        # Convert birth_date string to datetime
        birth_date_dt = parse_birth_date_from_cache(chart_data["birth_date"])
        
        # Get birth place information
        birth_place = f"{chart_data['city']}, {chart_data['nation']}"
        
        # First generate report to get structured data for interpretation
        report_data = report_service.generate_natal_report(
            name=chart_data["name"],
            birth_date=birth_date_dt,
            birth_place=birth_place,
            lat=chart_data["lat"],
            lng=chart_data["lng"],
            house_system=chart_data.get("houses_system", "Placidus"),
            timezone=chart_data.get("tz_str")
        )
        
        # Create a NatalReportData object from the report data dictionary
        natal_report_data = NatalReportData(
            title=report_data["title"],
            data_table=report_data["data_table"],
            planets_table=report_data["planets_table"],
            houses_table=report_data["houses_table"],
            full_report=report_data["full_report"]
        )
        
        # Generate interpretation using InterpretationService with structured data
        # Use run_in_threadpool for the blocking API call to Gemini
        interpretation_result = await run_in_threadpool(
            interpretation_service.interpret_natal_chart,
            report_data=natal_report_data,
            aspects_focus=aspects_focus,
            houses_focus=houses_focus,
            planets_focus=planets_focus,
            tone=tone,
            max_length=max_length
        )
        
        # Return the interpretation fragment
        return templates.TemplateResponse(
            "fragments/interpretation.html",
            {
                "request": request,
                **interpretation_result
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating interpretation: {str(e)}")
        return templates.TemplateResponse(
            "fragments/interpretation.html",
            {
                "request": request,
                "error": f"Error generating interpretation: {str(e)}"
            }
        )

@router.get("/download-report/{chart_id}", name="download_report")
async def download_report(
    chart_id: str,
    report_service: ReportServiceDep
):
    """
    Download a text report for a chart.
    
    Args:
        chart_id: The unique identifier for the chart
        report_service: ReportService dependency
        
    Returns:
        Text file with the chart report
    """
    try:
        # Get chart data from cache
        if chart_id not in chart_cache:
            raise HTTPException(status_code=404, detail="Chart not found")
        
        chart_data = chart_cache[chart_id]
        
        # Convert birth_date string to datetime
        birth_date_dt = parse_birth_date_from_cache(chart_data["birth_date"])
        
        # Get birth place information
        birth_place = f"{chart_data['city']}, {chart_data['nation']}"
        
        # Generate report using ReportService
        report_data = report_service.generate_natal_report(
            name=chart_data["name"],
            birth_date=birth_date_dt,
            birth_place=birth_place,
            lat=chart_data["lat"],
            lng=chart_data["lng"],
            house_system=chart_data.get("houses_system", "Placidus"),
            timezone=chart_data.get("tz_str")
        )
        
        # Use the full_report field from the dictionary
        full_report_text = report_data["full_report"]
        
        # Create response with the full report as plain text
        return Response(
            content=full_report_text,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={chart_id}_report.txt"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report for download: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.post("/search-location", response_class=HTMLResponse, name="search_location")
async def search_location(
    request: Request,
    geo_service: GeoServiceDep,
    city: Optional[str] = Form(None),
    hx_request: Optional[str] = Header(None)
):
    """
    Search for locations matching the city name.
    
    Args:
        request: The FastAPI request object
        geo_service: GeoService dependency
        city: City name to search for
        hx_request: HTMX request header
        
    Returns:
        HTML fragment with location search results
    """
    # Default context
    context = {
        "request": request,
        "locations": [],
        "city": city or "",
        "error": None
    }
    
    # Validate city input
    if not city or len(city.strip()) < 3:
        context["error"] = "Please enter at least 3 characters for city search"
        return templates.TemplateResponse("fragments/location_fields.html", context)
    
    try:
        # Use run_in_threadpool to run potentially blocking I/O operation in a separate thread
        # since the method is now synchronous but we're in an async route
        locations = await run_in_threadpool(geo_service.search_cities, city.strip(), 10)
        
        # Format results for the template
        context["locations"] = [
            {
                "name": loc.name,
                "country_code": loc.country_code,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "timezone": loc.timezone,
                "display": f"{loc.name}, {loc.country_code}"
            }
            for loc in locations
        ]
        
        # If HTMX request, return only the results fragment
        if hx_request:
            return templates.TemplateResponse("fragments/location_results.html", context)
        
        # Otherwise return the full fields
        return templates.TemplateResponse("fragments/location_fields.html", context)
        
    except Exception as e:
        context["error"] = f"Error searching locations: {str(e)}"
        if hx_request:
            return templates.TemplateResponse("fragments/location_results.html", context)
            
        return templates.TemplateResponse("fragments/location_fields.html", context)

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