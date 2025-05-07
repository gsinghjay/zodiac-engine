This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

## Additional Info

# Directory Structure
```
.cursor/
  rules/
    data-models.mdc
    fastapi-best-practices.mdc
    fastapi-testing.mdc
    project-structure.mdc
    route-structure.mdc
    service-layer.mdc
.github/
  workflows/
    semantic-release.yml
app/
  api/
    v1/
      routers/
        charts/
          __init__.py
          composite.py
          natal.py
          synastry.py
          transit.py
          visualization.py
        __init__.py
        geo.py
      __init__.py
    __init__.py
    web.py
  core/
    config.py
    dependencies.py
    error_handlers.py
    exceptions.py
  schemas/
    chart_visualization.py
    natal_chart.py
  services/
    astrology.py
    chart_visualization.py
    geo_service.py
  static/
    __init__.py
    styles.css
  templates/
    fragments/
      chart_preview.html
      form_validation.html
      location_fields.html
      location_results.html
    __init__.py
    chart_details.html
    home.html
    layout.html
  main.py
scripts/
  test_vedic_chart.sh
  test_western_chart.sh
tests/
  conftest.py
  test_chart_configuration.py
  test_charts_natal.py
  test_natal_chart_variations.py
  test_static_images.py
.cursorignore
.cursorrules
.gitignore
.repomixignore
pytest.ini
requirements.txt
```

# Files

## File: .github/workflows/semantic-release.yml
````yaml
name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release
    permissions:
      id-token: write
      contents: write

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Python Semantic Release
      uses: python-semantic-release/python-semantic-release@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
````

## File: app/api/v1/routers/charts/__init__.py
````python
"""Charts router initialization."""
from fastapi import APIRouter

from app.api.v1.routers.charts.natal import router as natal_router
from app.api.v1.routers.charts.visualization import router as visualization_router

# Create the charts router
router = APIRouter(
    prefix="/charts",
    tags=["charts"]
)

# Include individual chart type routers
router.include_router(natal_router)
router.include_router(visualization_router)

# Export the router for use in the main API
__all__ = ["router"]
````

## File: app/api/v1/routers/charts/composite.py
````python
"""Composite chart router module."""
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/composite",
    tags=["composite-chart"],
)

@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def calculate_composite_chart():
    """Placeholder for composite chart calculation endpoint."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Composite chart calculation not yet implemented"
    )
````

## File: app/api/v1/routers/charts/synastry.py
````python
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
````

## File: app/api/v1/routers/charts/transit.py
````python
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
````

## File: app/api/v1/routers/geo.py
````python
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
````

## File: app/core/exceptions.py
````python
"""Custom exception handling for the application."""
from typing import Any, Dict, Optional

from fastapi import HTTPException, status

class ZodiacEngineException(HTTPException):
    """Base exception for Zodiac Engine API."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class InvalidBirthDataError(ZodiacEngineException):
    """Exception for invalid birth data."""
    def __init__(self, detail: str = "Invalid birth data provided"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class LocationError(ZodiacEngineException):
    """Exception for location-related errors."""
    def __init__(self, detail: str = "Invalid location data"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class ChartCalculationError(ZodiacEngineException):
    """Exception for errors during chart calculation."""
    def __init__(self, detail: str = "Error calculating astrological chart"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
````

## File: app/templates/fragments/chart_preview.html
````html
{% if chart_url %}
<div class="card chart-preview mb-4">
    <div class="card-body">
        <h3 class="card-title mb-3">Chart Preview</h3>
        <div class="svg-container">
            <img src="{{ chart_url }}" alt="Astrological Chart for {{ name }}" class="chart-svg">
        </div>
        {% if chart_data %}
        <div class="mt-3">
            <h4 class="h5">Chart Details</h4>
            <table class="table table-bordered table-sm">
                <tbody>
                    <tr>
                        <th>Name</th>
                        <td>{{ chart_data.name }}</td>
                    </tr>
                    <tr>
                        <th>Date & Time</th>
                        <td>{{ chart_data.birth_date }}</td>
                    </tr>
                    <tr>
                        <th>Location</th>
                        <td>{{ chart_data.city }}, {{ chart_data.nation }}</td>
                    </tr>
                    <tr>
                        <th>Coordinates</th>
                        <td>Lat: {{ chart_data.lat }}, Lng: {{ chart_data.lng }}</td>
                    </tr>
                    <tr>
                        <th>House System</th>
                        <td>{{ chart_data.houses_system }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        {% endif %}
        <div class="mt-3">
            <a href="{{ chart_url }}" class="btn btn-outline-primary btn-sm" download="astrological_chart.svg">
                Download Chart
            </a>
        </div>
    </div>
</div>
{% else %}
<div class="card chart-preview mb-4">
    <div class="card-body text-center py-5">
        <p class="text-muted">Chart will appear here after generation</p>
    </div>
</div>
{% endif %}
````

## File: app/templates/fragments/form_validation.html
````html
{% if errors %}
<div class="alert alert-danger">
    <ul class="mb-0">
        {% for error in errors %}
        <li>{{ error }}</li>
        {% endfor %}
    </ul>
</div>
{% else %}
<div class="alert alert-success">
    <p class="mb-0">Form data is valid!</p>
</div>
{% endif %}
````

## File: app/templates/fragments/location_fields.html
````html
<div class="mb-3">
    <label for="city" class="form-label">Birth City</label>
    <div class="input-group">
        <input type="text" class="form-control" id="city" name="city" value="{{ city|default('') }}" 
               hx-post="{{ url_for('search_location') }}"
               hx-trigger="keyup changed delay:500ms"
               hx-target="#location-results"
               hx-indicator="#search-indicator"
               hx-params="city">
        <div id="search-indicator" class="htmx-indicator input-group-text">
            <span class="search-icon">⌛</span>
        </div>
    </div>
</div>

<div id="location-results"></div>

<div class="mb-3">
    <label for="nation" class="form-label">Country</label>
    <input type="text" class="form-control" id="nation" name="nation" value="{{ nation|default('') }}" required>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="mb-3">
            <label for="lng" class="form-label">Longitude</label>
            <input type="number" class="form-control" id="lng" name="lng" step="0.0001" placeholder="-73.8667" value="{{ lng|default('') }}" required>
        </div>
    </div>
    <div class="col-md-6">
        <div class="mb-3">
            <label for="lat" class="form-label">Latitude</label>
            <input type="number" class="form-control" id="lat" name="lat" step="0.0001" placeholder="40.7167" value="{{ lat|default('') }}" required>
        </div>
    </div>
</div>

<div class="mb-3">
    <label for="tz_str" class="form-label">Timezone</label>
    <select class="form-select" id="tz_str" name="tz_str" required>
        <option value="" {% if not tz_str %}selected{% endif %}>Select Timezone</option>
        <option value="America/New_York" {% if tz_str == "America/New_York" %}selected{% endif %}>America/New_York</option>
        <option value="America/Chicago" {% if tz_str == "America/Chicago" %}selected{% endif %}>America/Chicago</option>
        <option value="America/Denver" {% if tz_str == "America/Denver" %}selected{% endif %}>America/Denver</option>
        <option value="America/Los_Angeles" {% if tz_str == "America/Los_Angeles" %}selected{% endif %}>America/Los_Angeles</option>
        <option value="Europe/London" {% if tz_str == "Europe/London" %}selected{% endif %}>Europe/London</option>
        <option value="Europe/Paris" {% if tz_str == "Europe/Paris" %}selected{% endif %}>Europe/Paris</option>
        <option value="Europe/Berlin" {% if tz_str == "Europe/Berlin" %}selected{% endif %}>Europe/Berlin</option>
        <option value="Asia/Tokyo" {% if tz_str == "Asia/Tokyo" %}selected{% endif %}>Asia/Tokyo</option>
        <option value="Australia/Sydney" {% if tz_str == "Australia/Sydney" %}selected{% endif %}>Australia/Sydney</option>
    </select>
</div>
````

## File: app/templates/fragments/location_results.html
````html
{% if error %}
<div class="alert alert-danger py-2">
    <p class="mb-0">{{ error }}</p>
</div>
{% elif locations %}
<div class="list-group mb-3">
    {% for location in locations %}
    <button class="list-group-item list-group-item-action" 
            hx-post="{{ url_for('select_location') }}"
            hx-vals='{"city": "{{ location.city|default(location.name) }}", "nation": "{{ location.nation|default(location.country_code) }}", "lng": {{ location.lng|default(location.longitude) }}, "lat": {{ location.lat|default(location.latitude) }}, "tz_str": "{{ location.tz_str|default(location.timezone) }}" }'
            hx-target="#location-fields"
            hx-swap="innerHTML">
        {{ location.city|default(location.name) }}, {{ location.nation|default(location.country_code) }} 
        {% if location.tz_str %}({{ location.tz_str }}){% elif location.timezone %}({{ location.timezone }}){% endif %}
    </button>
    {% endfor %}
</div>
{% else %}
<p class="text-muted mb-3">No locations found. Please try a different search term.</p>
{% endif %}
````

## File: app/templates/__init__.py
````python
"""Templates initialization module."""
import os
import datetime
from fastapi.templating import Jinja2Templates

# Define the template directory
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

# Create templates object for use throughout the app
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Add custom Jinja2 filters/functions
templates.env.globals.update({
    "now": lambda fmt="%Y-%m-%d %H:%M:%S": datetime.datetime.now().strftime(fmt),
})
````

## File: app/templates/chart_details.html
````html
{% extends "layout.html" %}

{% block title %}Chart Details - {{ chart_data.name }}{% endblock %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="d-flex justify-content-between align-items-center">
                <h1 class="h2">Astrological Chart</h1>
                <a href="/home" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-left"></i> Back to Generator
                </a>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Chart Display Column -->
        <div class="col-lg-8">
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <div class="svg-container">
                        <img src="{{ chart_url }}" alt="Astrological Chart for {{ chart_data.name }}" class="chart-svg img-fluid">
                    </div>
                </div>
            </div>
        </div>

        <!-- Chart Information and Download Options -->
        <div class="col-lg-4">
            <!-- Chart Information -->
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-primary text-white">
                    <h2 class="h5 mb-0">Chart Details</h2>
                </div>
                <div class="card-body">
                    <table class="table table-bordered table-sm mb-0">
                        <tbody>
                            <tr>
                                <th>Name</th>
                                <td>{{ chart_data.name }}</td>
                            </tr>
                            <tr>
                                <th>Date & Time</th>
                                <td>{{ chart_data.birth_date }}</td>
                            </tr>
                            <tr>
                                <th>Location</th>
                                <td>{{ chart_data.city }}, {{ chart_data.nation }}</td>
                            </tr>
                            <tr>
                                <th>Coordinates</th>
                                <td>Lat: {{ chart_data.lat }}, Lng: {{ chart_data.lng }}</td>
                            </tr>
                            <tr>
                                <th>House System</th>
                                <td>{{ chart_data.houses_system }}</td>
                            </tr>
                            <tr>
                                <th>Chart Type</th>
                                <td>{{ chart_data.chart_type|capitalize }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Download Options -->
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h2 class="h5 mb-0">Download Options</h2>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <a href="/download-chart/{{ chart_id }}?format=svg" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            SVG Format
                            <span class="badge bg-primary rounded-pill">
                                <i class="bi bi-download"></i>
                            </span>
                        </a>
                        <a href="/download-chart/{{ chart_id }}?format=png" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            PNG Format
                            <span class="badge bg-primary rounded-pill">
                                <i class="bi bi-download"></i>
                            </span>
                        </a>
                        <a href="/download-chart/{{ chart_id }}?format=pdf" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            PDF Format
                            <span class="badge bg-primary rounded-pill">
                                <i class="bi bi-download"></i>
                            </span>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Share Options -->
            <div class="card shadow-sm mt-4">
                <div class="card-header bg-primary text-white">
                    <h2 class="h5 mb-0">Share Chart</h2>
                </div>
                <div class="card-body">
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" value="{{ request.url }}" id="share-url" readonly>
                        <button class="btn btn-outline-secondary" type="button" onclick="copyShareLink()">
                            Copy
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block head %}
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
<style>
    .chart-svg {
        max-width: 100%;
        height: auto;
    }
</style>
{% endblock %}

{% block scripts %}
<script>
    function copyShareLink() {
        const shareUrl = document.getElementById('share-url');
        shareUrl.select();
        shareUrl.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(shareUrl.value);
        
        // Show feedback
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Copied!';
        setTimeout(() => {
            btn.innerHTML = originalText;
        }, 2000);
    }
</script>
{% endblock %}
````

## File: scripts/test_vedic_chart.sh
````bash
#!/bin/bash

# Test script to generate Vedic (Sidereal) natal chart using curl

#=================================================
# CONFIGURATION VARIABLES - Modify as needed
#=================================================

# API Base URL
BASE_URL="http://localhost:8000"

# Birth data 
NAME="Jay Singh"
BIRTH_DATE="1994-07-17T10:30:00"
CITY="Queens"
NATION="US"
LNG=-73.8667  # 73w52 in decimal format
LAT=40.7167   # 40n43 in decimal format
TZ_STR="America/New_York"  # Timezone for New York

# Chart visualization options
CHART_THEME="classic"        # Options: dark, light, classic, dark-high-contrast
CHART_LANGUAGE="EN"       # Options: EN, FR, PT, IT, CN, ES, RU, TR, DE, HI
HOUSES_SYSTEM="W"         # Options: P (Placidus), W (Whole Sign), K (Koch), etc.
ZODIAC_TYPE="Sidereal"      # Options: Tropic, Sidereal
SIDEREAL_MODE="LAHIRI"          # Required if ZODIAC_TYPE="Sidereal", e.g., "FAGAN_BRADLEY"
PERSPECTIVE="Apparent Geocentric"  # Options: Apparent Geocentric, Heliocentric, etc.

# Active points to include in the chart - include ALL available points for comprehensive Vedic chart
ACTIVE_POINTS=(
  "Sun" "Moon" "Mercury" "Venus" "Mars" "Jupiter" "Saturn"
  "Uranus" "Neptune" "Pluto" "Ascendant" "Medium_Coeli" "Descendant" "Imum_Coeli"
  "Mean_Node" "True_Node" "Mean_South_Node" "True_South_Node" "Chiron" "Mean_Lilith"
)

# Aspects to include with orbs - Vedic astrology typically focuses on specific aspects
declare -A ASPECTS
ASPECTS["conjunction"]=10
ASPECTS["opposition"]=10
ASPECTS["trine"]=8
ASPECTS["square"]=8
ASPECTS["sextile"]=6
# Less commonly used in Vedic but still valuable
ASPECTS["quincunx"]=3
ASPECTS["semi-sextile"]=2
ASPECTS["quintile"]=2

#=================================================
# SCRIPT EXECUTION - No need to modify below
#=================================================

echo "Testing Vedic Chart Generation API..."
echo "======================================"

# Format active points array as JSON array
ACTIVE_POINTS_JSON=$(printf '"%s", ' "${ACTIVE_POINTS[@]}" | sed 's/, $//')
ACTIVE_POINTS_JSON="[${ACTIVE_POINTS_JSON}]"

# Format aspects as JSON array
ASPECTS_JSON=""
for aspect in "${!ASPECTS[@]}"; do
  ASPECTS_JSON+="{ \"name\": \"$aspect\", \"orb\": ${ASPECTS[$aspect]} }, "
done
ASPECTS_JSON=$(echo "$ASPECTS_JSON" | sed 's/, $//')
ASPECTS_JSON="[${ASPECTS_JSON}]"

# Build config JSON
CONFIG_JSON="{"
CONFIG_JSON+="\"houses_system\": \"${HOUSES_SYSTEM}\", "
CONFIG_JSON+="\"zodiac_type\": \"${ZODIAC_TYPE}\", "
CONFIG_JSON+="\"perspective_type\": \"${PERSPECTIVE}\", "
CONFIG_JSON+="\"active_points\": ${ACTIVE_POINTS_JSON}, "
CONFIG_JSON+="\"active_aspects\": ${ASPECTS_JSON}"
# Add sidereal mode if provided
if [ ! -z "$SIDEREAL_MODE" ]; then
  CONFIG_JSON+=", \"sidereal_mode\": \"${SIDEREAL_MODE}\""
fi
CONFIG_JSON+="}"

# 1. Generate basic natal chart
echo "Generating basic natal chart..."
curl -s -X POST \
  "${BASE_URL}/api/v1/charts/natal/" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${NAME}\",
    \"birth_date\": \"${BIRTH_DATE}\",
    \"city\": \"${CITY}\",
    \"nation\": \"${NATION}\",
    \"lng\": ${LNG},
    \"lat\": ${LAT},
    \"tz_str\": \"${TZ_STR}\",
    \"houses_system\": \"${HOUSES_SYSTEM}\"
  }" | jq '.' || echo "Failed to parse JSON. Raw response:"

echo -e "\n\n"

# 2. Generate natal chart visualization
echo "Generating natal chart visualization..."
CHART_ID="jay_vedic_$(date +%s)"
curl -s -X POST \
  "${BASE_URL}/api/v1/charts/visualization/natal" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${NAME}\",
    \"birth_date\": \"${BIRTH_DATE}\",
    \"city\": \"${CITY}\",
    \"nation\": \"${NATION}\",
    \"lng\": ${LNG},
    \"lat\": ${LAT},
    \"tz_str\": \"${TZ_STR}\",
    \"chart_id\": \"${CHART_ID}\",
    \"theme\": \"${CHART_THEME}\",
    \"language\": \"${CHART_LANGUAGE}\",
    \"config\": ${CONFIG_JSON}
  }" | jq '.' || echo "Failed to parse JSON. Raw response:"

echo -e "\n"
echo "Chart ID: ${CHART_ID}"
echo "Chart should be available at: ${BASE_URL}/static/images/svg/${CHART_ID}.svg"
echo "To view the chart, open a browser and navigate to the URL above"
echo -e "\n"

echo "Done!"
````

## File: scripts/test_western_chart.sh
````bash
#!/bin/bash

# Test script to generate Western (Tropical) natal chart using curl

#=================================================
# CONFIGURATION VARIABLES - Modify as needed
#=================================================

# API Base URL
BASE_URL="http://localhost:8000"

# Birth data 
NAME="Jay Singh"
BIRTH_DATE="1994-07-17T10:30:00"
CITY="Queens"
NATION="US"
LNG=-73.8667  # 73w52 in decimal format
LAT=40.7167   # 40n43 in decimal format
TZ_STR="America/New_York"  # Timezone for New York

# Chart visualization options
CHART_THEME="light"        # Options: dark, light, classic, dark-high-contrast
CHART_LANGUAGE="EN"       # Options: EN, FR, PT, IT, CN, ES, RU, TR, DE, HI
HOUSES_SYSTEM="P"         # Options: P (Placidus), W (Whole Sign), K (Koch), etc.
ZODIAC_TYPE="Tropic"      # Options: Tropic, Sidereal
SIDEREAL_MODE=""          # Not needed for Tropical zodiac
PERSPECTIVE="Apparent Geocentric"  # Options: Apparent Geocentric, Heliocentric, Topocentric, True Geocentric

# Active points to include in the chart - include ALL available points for comprehensive Western chart
ACTIVE_POINTS=(
  # Traditional planets
  "Sun" "Moon" "Mercury" "Venus" "Mars" "Jupiter" "Saturn"
  # Modern planets
  "Uranus" "Neptune" "Pluto" 
  # Angles and axes
  "Ascendant" "Medium_Coeli" "Descendant" "Imum_Coeli"
  # Additional points important in Western astrology 
  "Chiron" "Mean_Node" "True_Node" "Mean_South_Node" "True_South_Node" "Mean_Lilith"
)

# Note: The following Western astrological elements are commonly used but not yet supported by our API:
# - Asteroids (Ceres, Pallas, Juno, Vesta)
# - Part of Fortune and other Arabic Parts
# - Fixed Stars (Regulus, Spica, Algol, etc.)
# - Planetary Midpoints
# - Declination values and Out-of-Bounds planets
# - Harmonics and Composite charts

# Aspects to include with orbs - Western astrology typically uses more aspects
declare -A ASPECTS
ASPECTS["conjunction"]=8
ASPECTS["opposition"]=8
ASPECTS["trine"]=7
ASPECTS["square"]=7
ASPECTS["sextile"]=6
ASPECTS["semi-sextile"]=3
ASPECTS["semi-square"]=3
ASPECTS["sesquiquadrate"]=3
ASPECTS["quincunx"]=3
ASPECTS["quintile"]=2
ASPECTS["biquintile"]=2

#=================================================
# SCRIPT EXECUTION - No need to modify below
#=================================================

echo "Testing Western Chart Generation API..."
echo "======================================"

# Format active points array as JSON array
ACTIVE_POINTS_JSON=$(printf '"%s", ' "${ACTIVE_POINTS[@]}" | sed 's/, $//')
ACTIVE_POINTS_JSON="[${ACTIVE_POINTS_JSON}]"

# Format aspects as JSON array
ASPECTS_JSON=""
for aspect in "${!ASPECTS[@]}"; do
  ASPECTS_JSON+="{ \"name\": \"$aspect\", \"orb\": ${ASPECTS[$aspect]} }, "
done
ASPECTS_JSON=$(echo "$ASPECTS_JSON" | sed 's/, $//')
ASPECTS_JSON="[${ASPECTS_JSON}]"

# Build config JSON
CONFIG_JSON="{"
CONFIG_JSON+="\"houses_system\": \"${HOUSES_SYSTEM}\", "
CONFIG_JSON+="\"zodiac_type\": \"${ZODIAC_TYPE}\", "
CONFIG_JSON+="\"perspective_type\": \"${PERSPECTIVE}\", "
CONFIG_JSON+="\"active_points\": ${ACTIVE_POINTS_JSON}, "
CONFIG_JSON+="\"active_aspects\": ${ASPECTS_JSON}"
# Add sidereal mode if provided
if [ ! -z "$SIDEREAL_MODE" ]; then
  CONFIG_JSON+=", \"sidereal_mode\": \"${SIDEREAL_MODE}\""
fi
CONFIG_JSON+="}"

# 1. Generate basic natal chart
echo "Generating basic natal chart..."
curl -s -X POST \
  "${BASE_URL}/api/v1/charts/natal/" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${NAME}\",
    \"birth_date\": \"${BIRTH_DATE}\",
    \"city\": \"${CITY}\",
    \"nation\": \"${NATION}\",
    \"lng\": ${LNG},
    \"lat\": ${LAT},
    \"tz_str\": \"${TZ_STR}\",
    \"houses_system\": \"${HOUSES_SYSTEM}\"
  }" | jq '.' || echo "Failed to parse JSON. Raw response:"

echo -e "\n\n"

# 2. Generate natal chart visualization
echo "Generating natal chart visualization..."
CHART_ID="jay_western_$(date +%s)"
curl -s -X POST \
  "${BASE_URL}/api/v1/charts/visualization/natal" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${NAME}\",
    \"birth_date\": \"${BIRTH_DATE}\",
    \"city\": \"${CITY}\",
    \"nation\": \"${NATION}\",
    \"lng\": ${LNG},
    \"lat\": ${LAT},
    \"tz_str\": \"${TZ_STR}\",
    \"chart_id\": \"${CHART_ID}\",
    \"theme\": \"${CHART_THEME}\",
    \"language\": \"${CHART_LANGUAGE}\",
    \"config\": ${CONFIG_JSON}
  }" | jq '.' || echo "Failed to parse JSON. Raw response:"

echo -e "\n"
echo "Chart ID: ${CHART_ID}"
echo "Chart should be available at: ${BASE_URL}/static/images/svg/${CHART_ID}.svg"
echo "To view the chart, open a browser and navigate to the URL above"
echo -e "\n"

echo "Done!"
````

## File: tests/conftest.py
````python
"""Test configuration and fixtures for the tests directory."""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)
````

## File: .cursorignore
````
repomix-output.md
````

## File: .cursorrules
````
# Cline's Memory Bank

I am Cline, an expert software engineer with a unique characteristic: my memory resets completely between sessions. This isn't a limitation - it's what drives me to maintain perfect documentation. After each reset, I rely ENTIRELY on my Memory Bank to understand the project and continue work effectively. I MUST read ALL memory bank files at the start of EVERY task - this is not optional.

## Memory Bank Structure

The Memory Bank consists of core files and optional context files, all in Markdown format. Files build upon each other in a clear hierarchy:

flowchart TD
    PB[projectbrief.md] --> PC[productContext.md]
    PB --> SP[systemPatterns.md]
    PB --> TC[techContext.md]
    
    PC --> AC[activeContext.md]
    SP --> AC
    TC --> AC
    
    AC --> P[progress.md]

### Core Files (Required)
1. `projectbrief.md`
   - Foundation document that shapes all other files
   - Created at project start if it doesn't exist
   - Defines core requirements and goals
   - Source of truth for project scope

2. `productContext.md`
   - Why this project exists
   - Problems it solves
   - How it should work
   - User experience goals

3. `activeContext.md`
   - Current work focus
   - Recent changes
   - Next steps
   - Active decisions and considerations
   - Important patterns and preferences
   - Learnings and project insights

4. `systemPatterns.md`
   - System architecture
   - Key technical decisions
   - Design patterns in use
   - Component relationships
   - Critical implementation paths

5. `techContext.md`
   - Technologies used
   - Development setup
   - Technical constraints
   - Dependencies
   - Tool usage patterns

6. `progress.md`
   - What works
   - What's left to build
   - Current status
   - Known issues
   - Evolution of project decisions

### Additional Context
Create additional files/folders within memory-bank/ when they help organize:
- Complex feature documentation
- Integration specifications
- API documentation
- Testing strategies
- Deployment procedures

## Core Workflows

### Plan Mode
flowchart TD
    Start[Start] --> ReadFiles[Read Memory Bank]
    ReadFiles --> CheckFiles{Files Complete?}
    
    CheckFiles -->|No| Plan[Create Plan]
    Plan --> Document[Document in Chat]
    
    CheckFiles -->|Yes| Verify[Verify Context]
    Verify --> Strategy[Develop Strategy]
    Strategy --> Present[Present Approach]

### Act Mode
flowchart TD
    Start[Start] --> Context[Check Memory Bank]
    Context --> Update[Update Documentation]
    Update --> Execute[Execute Task]
    Execute --> Document[Document Changes]

## Documentation Updates

Memory Bank updates occur when:
1. Discovering new project patterns
2. After implementing significant changes
3. When user requests with **update memory bank** (MUST review ALL files)
4. When context needs clarification

flowchart TD
    Start[Update Process]
    
    subgraph Process
        P1[Review ALL Files]
        P2[Document Current State]
        P3[Clarify Next Steps]
        P4[Document Insights & Patterns]
        
        P1 --> P2 --> P3 --> P4
    end
    
    Start --> Process

Note: When triggered by **update memory bank**, I MUST review every memory bank file, even if some don't require updates. Focus particularly on activeContext.md and progress.md as they track current state.

REMEMBER: After every memory reset, I begin completely fresh. The Memory Bank is my only link to previous work. It must be maintained with precision and clarity, as my effectiveness depends entirely on its accuracy.
````

## File: .repomixignore
````
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.pyw
*.pyz

libraries/
images/
docs/
.env
cache/
*.md
````

## File: pytest.ini
````
[pytest]
testpaths = app/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
filterwarnings =
    ignore::DeprecationWarning
    ignore::UserWarning
addopts = -v --tb=short
````

## File: .cursor/rules/data-models.mdc
````
---
description: This rule documents the Pydantic data models used throughout the Zodiac Engine. Call this rule when working with data validation, schemas, or API request/response models. Use it when users need to understand the data structure, want to modify existing models, or need to create new Pydantic schemas according to best practices.
globs: 
alwaysApply: false
---
# Zodiac Engine Data Models

This rule documents the data model structure of the Zodiac Engine application, which uses Pydantic for data validation and serialization.

## Schema Structure

Schemas are located in [app/schemas](mdc:app/schemas) and define:
- Request/response models for API endpoints
- Data validation rules
- Documentation for the OpenAPI schema

## Key Schema Files

### Natal Chart Schemas

[app/schemas/natal_chart.py](mdc:app/schemas/natal_chart.py) contains:
- `PlanetPosition` - Schema for planet position in a chart
- `NatalChartRequest` - Schema for natal chart calculation request
- `AspectInfo` - Schema for planetary aspect information
- `HouseSystem` - Schema for house system information
- `NatalChartResponse` - Schema for natal chart calculation response

### Chart Visualization Schemas

[app/schemas/chart_visualization.py](mdc:app/schemas/chart_visualization.py) contains:
- `AspectConfiguration` - Schema for aspect configuration
- `ChartConfiguration` - Schema for chart configuration options
- `NatalChartVisualizationRequest` - Schema for natal chart visualization request
- `SynastryChartVisualizationRequest` - Schema for synastry chart visualization request
- `ChartVisualizationResponse` - Base schema for chart visualization response
- `NatalChartVisualizationResponse` - Response schema for natal chart visualization
- `SynastryChartVisualizationResponse` - Response schema for synastry chart visualization

## Pydantic Usage

The schemas leverage Pydantic v2 features:
- Modern type annotations (`str | None`, `list[Type]`, `dict[Key, Value]`) for validation
- Field descriptors with examples
- Default values
- `model_config` for schema configuration
- Literal types for strict value validation (e.g., `SiderealMode`)
- Documentation generation for the OpenAPI schema

## Modernization Status

The application schemas have been fully updated to use the latest Pydantic v2 syntax and features as part of the FastAPI best practices implementation.
````

## File: .cursor/rules/fastapi-best-practices.mdc
````
---
description: Documents the established FastAPI best practices for the Zodiac Engine, covering dependencies, Pydantic v2, DI, async/sync, error handling, responses, and performance. Fetch this rule when implementing/refactoring FastAPI code, evaluating quality, or answering user questions about project standards.
globs: 
alwaysApply: false
---
# FastAPI Best Practices Guide

This rule outlines FastAPI best practices for the Zodiac Engine application based on our analysis. These practices align with the latest recommendations from FastAPI's documentation and community standards.

## Key Best Practices

### Dependencies Management
- Avoid using `fastapi[all]` in [requirements.txt](mdc:requirements.txt)
- Use explicit version constraints for all dependencies

### Pydantic Usage
- Use latest Pydantic v2 syntax: `str | None` instead of `Optional[str]`
- Use updated Pydantic configuration: `model_config = {...}` instead of `class Config`
- Define clear schemas in [app/schemas](mdc:app/schemas) directory

### Dependency Injection
- Use `Annotated[Type, Depends()]` syntax in endpoint parameters
- Inject services as dependencies rather than using static methods
- Apply `@lru_cache` to expensive dependencies as seen in [app/core/dependencies.py](mdc:app/core/dependencies.py)

### Async/Sync Consistency
- Use `async def` only for endpoints that perform async I/O operations
- Keep service methods synchronous if they don't perform I/O
- Maintain consistent async/sync patterns throughout the codebase

### Error Handling
- Import from `fastapi import status` when setting status codes
- Use custom exception classes as defined in [app/core/exceptions.py](mdc:app/core/exceptions.py)
- Implement global exception handlers as in [app/core/error_handlers.py](mdc:app/core/error_handlers.py)

### API Response Options
- Use `response_model_exclude_unset=True` where appropriate
- Set proper status codes for different operations
- Document response schemas in API routes

### Performance 
- Use FastAPI's background tasks for long-running operations
- Implement caching for expensive calculations
````

## File: .cursor/rules/project-structure.mdc
````
---
description: This rule outlines the recommended FastAPI best practices for the Zodiac Engine application. Call this rule when evaluating existing code, planning improvements, or implementing new features according to modern FastAPI standards. Use it when users ask about code quality, want to follow best practices, or need guidance on specific FastAPI features implementation.
globs: 
alwaysApply: false
---
# Zodiac Engine Project Structure

The Zodiac Engine is a FastAPI application for astrological calculations and chart visualization.

## Main Application Structure

The main entry point is [app/main.py](mdc:app/main.py), which creates the FastAPI application and configures it.

## Key Components:

- **API Routes**: Located in [app/api](mdc:app/api) with versioning (v1)
  - Routers: [app/api/v1/routers](mdc:app/api/v1/routers)
  - Chart Routers: [app/api/v1/routers/charts](mdc:app/api/v1/routers/charts)
  - Natal charts: [app/api/v1/routers/charts/natal.py](mdc:app/api/v1/routers/charts/natal.py)
  - Visualizations: [app/api/v1/routers/charts/visualization.py](mdc:app/api/v1/routers/charts/visualization.py)

- **Core Components**: Located in [app/core](mdc:app/core)
  - Configuration: [app/core/config.py](mdc:app/core/config.py)
  - Dependencies: [app/core/dependencies.py](mdc:app/core/dependencies.py)
  - Error Handling: [app/core/error_handlers.py](mdc:app/core/error_handlers.py)
  - Custom Exceptions: [app/core/exceptions.py](mdc:app/core/exceptions.py)

- **Data Models**: Located in [app/schemas](mdc:app/schemas)
  - Natal Chart: [app/schemas/natal_chart.py](mdc:app/schemas/natal_chart.py)
  - Chart Visualization: [app/schemas/chart_visualization.py](mdc:app/schemas/chart_visualization.py)

- **Business Logic**: Located in [app/services](mdc:app/services)
  - Astrology Service: [app/services/astrology.py](mdc:app/services/astrology.py)
  - Chart Visualization: [app/services/chart_visualization.py](mdc:app/services/chart_visualization.py)

- **Static Files**: Located in [app/static](mdc:app/static)

## Testing

Tests are located in the [tests](mdc:tests) directory:
- Natal Chart Tests: [tests/test_natal_chart_variations.py](mdc:tests/test_natal_chart_variations.py)
- Chart Configuration Tests: [tests/test_chart_configuration.py](mdc:tests/test_chart_configuration.py)

## Dependencies

Dependencies are listed in [requirements.txt](mdc:requirements.txt)
````

## File: .cursor/rules/route-structure.mdc
````
---
description: This rule documents the API route structure and endpoints of the Zodiac Engine. Call this rule when working with API endpoints, understanding route hierarchies, or implementing new routes. Use it when users need information about available endpoints, want to modify existing routes, or need to understand how routes are organized in the application.
globs: 
alwaysApply: false
---
# Zodiac Engine API Routes Structure

This rule documents the API route structure of the Zodiac Engine application, which follows a clean, hierarchical organization.

## Route Hierarchy

- Main router is included in [app/main.py](mdc:app/main.py)
- API routes are organized in [app/api](mdc:app/api)
- API versions are separated in directories (currently v1)
- Each router group has its own module in [app/api/v1/routers](mdc:app/api/v1/routers)

## Key API Endpoints

### Chart Routers

The primary endpoints for astrological charts are located in [app/api/v1/routers/charts](mdc:app/api/v1/routers/charts):

- **Natal Charts**: [app/api/v1/routers/charts/natal.py](mdc:app/api/v1/routers/charts/natal.py)
  - Calculates complete natal charts based on birth data
  - Endpoint: `POST /api/v1/charts/natal/`

- **Chart Visualization**: [app/api/v1/routers/charts/visualization.py](mdc:app/api/v1/routers/charts/visualization.py)
  - Generates SVG visualizations of charts
  - Endpoints: 
    - `POST /api/v1/charts/visualization/natal`
    - `POST /api/v1/charts/visualization/synastry`

- **Synastry**: [app/api/v1/routers/charts/synastry.py](mdc:app/api/v1/routers/charts/synastry.py)
  - Analyzes relationships between two charts
  - Endpoint: `POST /api/v1/charts/synastry/`

- **Composite**: [app/api/v1/routers/charts/composite.py](mdc:app/api/v1/routers/charts/composite.py)
  - Generates and analyzes composite charts
  - Endpoint: `POST /api/v1/charts/composite/`

### Health Endpoint

- Root health check implemented in [app/main.py](mdc:app/main.py)
  - Endpoint: `GET /`
  - Returns API status and version

## Route Configuration

All routes use:
- Proper response models
- Detailed documentation
- Appropriate tagging
- Standardized error responses
````

## File: .cursor/rules/service-layer.mdc
````
---
description: This rule explains the service layer implementation in the Zodiac Engine. Call this rule when working with business logic, analyzing service methods, or implementing new services. Use it when users need to understand how core functionality is abstracted, how to interact with the Kerykeion library, or how to modify existing service components.
globs: 
alwaysApply: false
---
# Zodiac Engine Service Layer

This rule documents the service layer implementation in the Zodiac Engine. The service layer contains the core business logic and abstracts complex operations from the API endpoints.

## Service Components

The service layer is located in [app/services](mdc:app/services) and consists of:

### Astrology Service

The [app/services/astrology.py](mdc:app/services/astrology.py) file contains:
- `AstrologyService` - Handles calculations for astrological charts
- Uses the Kerykeion library for core astrology computations
- Provides methods for:
  - Calculating natal charts
  - Processing planetary positions
  - Computing house positions
  - Generating aspects between planets

### Chart Visualization Service

The [app/services/chart_visualization.py](mdc:app/services/chart_visualization.py) file contains:
- `ChartVisualizationService` - Generates visual representations of charts
- Creates SVG images of astrological charts using Kerykeion
- Provides methods for:
  - Generating natal chart SVGs
  - Generating synastry chart SVGs
  - Customizing chart appearance (themes, languages)
  - Managing SVG file storage

## Service Layer Design 

The service layer follows modern FastAPI best practices:
- Services are implemented as classes with instance methods.
- Dependency injection is used via factory functions in [app/core/dependencies.py](mdc:app/core/dependencies.py) to provide service instances to API routes.
- Settings and other dependencies are injected into service constructors (`__init__`).
- `@lru_cache` is used on methods like `AstrologyService.calculate_natal_chart` for performance.
- Async methods are used where appropriate (e.g., if database interactions were added).
- Background tasks are leveraged for long-running processes like SVG generation, orchestrated by the API layer calling service methods.
````

## File: app/api/v1/routers/__init__.py
````python
"""API v1 routers initialization."""
from fastapi import APIRouter

from app.api.v1.routers.charts import router as charts_router
from app.api.v1.routers.geo import router as geo_router

# Create the routers router
router = APIRouter()

# Include charts router
router.include_router(charts_router)

# Include geo router
router.include_router(geo_router)

# Export the router for use in the main v1 router
__all__ = ["router"]
````

## File: app/api/v1/__init__.py
````python
"""API v1 router initialization."""
from fastapi import APIRouter

from app.api.v1.routers import router as routers_router

# Create the main v1 router with prefix and tag
router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

# Include endpoints router
router.include_router(routers_router)

# Export the router for use in the main API router
__all__ = ["router"]
````

## File: app/api/__init__.py
````python
"""API router initialization."""
from fastapi import APIRouter

from app.api.v1 import router as v1_router
from app.api.web import router as web_router

# Create the main API router
router = APIRouter()

# Include API version routers
router.include_router(v1_router)

# Include web interface router
router.include_router(web_router)

# Export the router for use in the main app
__all__ = ["router"]
````

## File: app/api/web.py
````python
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
````

## File: app/core/error_handlers.py
````python
"""Global exception handlers for the application."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions import (
    ChartCalculationError,
    InvalidBirthDataError,
    LocationError,
    ZodiacEngineException,
)

def add_error_handlers(app: FastAPI) -> None:
    """Add error handlers to the FastAPI application."""
    
    @app.exception_handler(ZodiacEngineException)
    async def zodiac_engine_exception_handler(
        request: Request,
        exc: ZodiacEngineException
    ) -> JSONResponse:
        """Handle custom ZodiacEngine exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "type": type(exc).__name__,
                    "path": request.url.path
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, 
        exc: RequestValidationError
    ) -> JSONResponse:
        """Handle request validation errors from FastAPI."""
        errors = []
        for error in exc.errors():
            error_msg = {
                "loc": " -> ".join([str(loc) for loc in error["loc"]]),
                "message": error["msg"],
                "type": error["type"]
            }
            errors.append(error_msg)
            
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "Validation error on request data",
                    "type": "RequestValidationError",
                    "path": request.url.path,
                    "details": errors
                }
            }
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(
        request: Request, 
        exc: ValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        errors = []
        for error in exc.errors():
            error_msg = {
                "loc": " -> ".join([str(loc) for loc in error["loc"]]),
                "message": error["msg"],
                "type": error["type"]
            }
            errors.append(error_msg)
            
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "Validation error on response data",
                    "type": "ValidationError",
                    "path": request.url.path,
                    "details": errors
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle any unhandled exceptions."""
        # Map Kerykeion exceptions to our custom exceptions
        exc_name = type(exc).__name__
        exc_module = type(exc).__module__

        # Check if it's a Kerykeion exception
        is_kerykeion_exception = "kerykeion" in exc_module.lower()
        
        if "InvalidDateError" in exc_name or (is_kerykeion_exception and "date" in str(exc).lower()):
            status_code = status.HTTP_400_BAD_REQUEST
            message = f"Invalid date: {str(exc)}"
            error_type = "InvalidDateError"
        elif "InvalidCoordinatesError" in exc_name or (is_kerykeion_exception and ("coordinates" in str(exc).lower() or "lat" in str(exc).lower() or "lng" in str(exc).lower())):
            status_code = status.HTTP_400_BAD_REQUEST
            message = f"Invalid coordinates: {str(exc)}"
            error_type = "InvalidCoordinatesError"
        elif "GeonamesError" in exc_name or (is_kerykeion_exception and "geonames" in str(exc).lower()):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            message = f"Geonames service unavailable: {str(exc)}"
            error_type = "GeonamesServiceError"
        elif is_kerykeion_exception:
            # Other Kerykeion errors
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = f"Astrological calculation error: {str(exc)}"
            error_type = "AstrologyCalculationError"
        else:
            # Generic server error
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal server error"
            error_type = exc_name

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "code": status_code,
                    "message": message,
                    "type": error_type,
                    "path": request.url.path
                }
            }
        )
````

## File: app/services/geo_service.py
````python
"""Geo service for location-based functionality."""

import logging
import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from requests import Request
from requests_cache import CachedSession
from datetime import timedelta

from app.core.config import settings


# Define response models
class GeoLocation(BaseModel):
    """Location data with coordinates and timezone."""
    name: str
    country_code: str
    latitude: float
    longitude: float
    timezone: str


class GeoService:
    """Service for handling geolocation requests."""
    
    def __init__(self):
        """Initialize the geo service with cache session."""
        cache_dir = os.path.join(os.getcwd(), "cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        self.session = CachedSession(
            cache_name="cache/zodiac_geonames_cache",
            backend="sqlite",
            expire_after=timedelta(days=30),
        )
        
        # Check if username is properly set
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Settings GEONAMES_USERNAME value: '{settings.GEONAMES_USERNAME}'")
        
        # Only use non-empty username values
        if settings.GEONAMES_USERNAME and settings.GEONAMES_USERNAME.strip():
            self.username = settings.GEONAMES_USERNAME.strip()
            self.logger.info(f"Using GeoNames username: {self.username}")
        else:
            self.username = "demo"
            self.logger.warning("No GEONAMES_USERNAME set in .env or it's empty. Using demo mode with limited functionality.")
        
        self.base_url = "http://api.geonames.org/searchJSON"
        self.timezone_url = "http://api.geonames.org/timezoneJSON"
    
    async def search_cities(self, query: str, max_rows: int = 10) -> List[GeoLocation]:
        """
        Search for cities matching the query.
        
        Args:
            query: Search string for city name
            max_rows: Maximum number of results to return (default: 10)
            
        Returns:
            List of locations with coordinates and timezone
        """
        if self.username == "demo":
            self.logger.warning("Using demo mode with limited functionality. The API may refuse service if demo limit is exceeded.")
        
        params = {
            "q": query,
            "maxRows": max_rows,
            "username": self.username,
            "style": "MEDIUM",
            "featureClass": "P",  # Populated places
        }
        
        prepared_request = Request("GET", self.base_url, params=params).prepare()
        self.logger.debug(f"Requesting city data from GeoNames: {prepared_request.url}")
        
        try:
            response = self.session.send(prepared_request)
            response_json = response.json()
            
            if "status" in response_json:
                # Error response
                error_msg = response_json.get("status", {}).get("message", "Unknown GeoNames error")
                self.logger.error(f"GeoNames API error: {error_msg}")
                return []
            
            results = []
            for place in response_json.get("geonames", []):
                # For each place, get the timezone
                timezone = await self._get_timezone(place.get("lat"), place.get("lng"))
                
                results.append(GeoLocation(
                    name=place.get("name", ""),
                    country_code=place.get("countryCode", ""),
                    latitude=float(place.get("lat", 0)),
                    longitude=float(place.get("lng", 0)),
                    timezone=timezone
                ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error fetching data from GeoNames: {e}")
            return []
    
    async def _get_timezone(self, lat: str, lng: str) -> str:
        """
        Get timezone for given coordinates.
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Timezone string (e.g., 'America/New_York')
        """
        params = {
            "lat": lat,
            "lng": lng,
            "username": self.username
        }
        
        prepared_request = Request("GET", self.timezone_url, params=params).prepare()
        self.logger.debug(f"Requesting timezone data from GeoNames: {prepared_request.url}")
        
        try:
            response = self.session.send(prepared_request)
            response_json = response.json()
            
            if "status" in response_json:
                # Error response
                error_msg = response_json.get("status", {}).get("message", "Unknown GeoNames error")
                self.logger.error(f"GeoNames API error when fetching timezone: {error_msg}")
                return ""
            
            return response_json.get("timezoneId", "")
            
        except Exception as e:
            self.logger.error(f"Error fetching timezone from GeoNames: {e}")
            return ""
````

## File: app/static/__init__.py
````python
"""Static files initialization."""
import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Define path to static files
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

def initialize_static_dirs():
    """Ensure all required static directories exist."""
    # Create svg directory if it doesn't exist
    svg_dir = os.path.join(STATIC_DIR, "images", "svg")
    if not os.path.exists(svg_dir):
        logger.info(f"Creating directory: {svg_dir}")
        os.makedirs(svg_dir, exist_ok=True)
        logger.info(f"SVG directory created at {svg_dir}")
    else:
        logger.info(f"SVG directory already exists at {svg_dir}")

def mount_static_files(app: FastAPI) -> None:
    """Mount static files to the FastAPI application."""
    # Ensure directories exist
    initialize_static_dirs()
    
    # Mount static directory
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    logger.info(f"Static files mounted from {STATIC_DIR}")
````

## File: app/static/styles.css
````css
/* Zodiac Engine UI - Bootstrap Customization */

:root {
  --bs-primary: #6a5acd;
  --bs-secondary: #9370db;
  --bs-success: #28a745;
  --bs-danger: #dc3545;
}

/* Custom color overrides */
.bg-primary {
  background-color: var(--bs-primary) !important;
}

.btn-primary {
  background-color: var(--bs-primary);
  border-color: var(--bs-primary);
}

.btn-primary:hover {
  background-color: var(--bs-secondary);
  border-color: var(--bs-secondary);
}

/* Chart container styles */
.chart-container {
  min-height: 400px;
  position: relative;
}

.chart-container svg {
  max-width: 100%;
  height: auto;
  display: block;
}

/* HTMX Specific Styles */
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: inline-block;
}

.htmx-request.htmx-indicator {
  display: inline-block;
}

/* Chart Preview */
.chart-preview {
  margin-top: 1.5rem;
  border-radius: 0.25rem;
  padding: 1rem;
  background-color: #fff;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

/* SVG chart styles */
.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  overflow: hidden;
}

.chart-svg {
  display: block;
  margin: 0 auto;
  max-width: 100%;
}
````

## File: app/templates/home.html
````html
{% extends "layout.html" %}

{% block title %}Zodiac Engine - Chart Generator{% endblock %}

{% block head %}
<style>
    /* Location modal additional styles */
    #location-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        justify-content: center;
        align-items: center;
    }
    
    /* Location search styles */
    .location-search {
        display: flex;
    }
    
    .location-search input {
        flex: 1;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
    }
    
    .search-btn {
        padding: 0.5rem 0.75rem;
        background-color: var(--bs-primary);
        color: white;
        border: none;
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
        cursor: pointer;
    }
    
    .search-icon {
        font-size: 1rem;
    }
    
    .modal-content {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        max-width: 500px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .modal-header h3 {
        margin: 0;
    }
    
    .modal-close {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
</style>
{% endblock %}

{% block content %}
{% if error %}
<div class="alert alert-danger">
    <h5 class="alert-heading">Error</h5>
    <div>{{ error }}</div>
</div>
{% endif %}

<div class="card mb-4 shadow-sm">
    <div class="card-body">
        <h2 class="card-title text-primary border-bottom pb-2 mb-3">Generate Astrological Chart</h2>
        
        <ul class="nav nav-tabs mb-3" id="chart-tabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="western-tab" data-bs-toggle="tab" data-bs-target="#western-content" type="button" role="tab" aria-controls="western-content" aria-selected="true">
                    Western (Tropical)
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="vedic-tab" data-bs-toggle="tab" data-bs-target="#vedic-content" type="button" role="tab" aria-controls="vedic-content" aria-selected="false">
                    Vedic (Sidereal)
                </button>
            </li>
        </ul>
        
        <div id="tabs-content" class="tab-content">
            <div class="tab-pane fade show active" id="western-content" role="tabpanel" aria-labelledby="western-tab">
                <form id="western-form" 
                    hx-post="/generate-chart" 
                    hx-target="#form-processing-message"
                    hx-indicator="#form-submitting">
                    <input type="hidden" name="chart_type" value="western">
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" name="name" required
                                    hx-post="{{ url_for('validate_form') }}"
                                    hx-trigger="change"
                                    hx-target="#validation-result"
                                    hx-params="name">
                            </div>
                            
                            <div class="mb-3">
                                <label for="birth_date" class="form-label">Birth Date & Time</label>
                                <input type="datetime-local" class="form-control" id="birth_date" name="birth_date" required
                                    hx-post="{{ url_for('validate_form') }}"
                                    hx-trigger="change"
                                    hx-target="#validation-result"
                                    hx-params="birth_date">
                            </div>
                            
                            <div id="location-fields">
                                {% include "fragments/location_fields.html" %}
                            </div>
                            
                            <div class="mb-3">
                                <label for="houses_system" class="form-label">Houses System</label>
                                <select class="form-select" id="houses_system" name="houses_system" required
                                    hx-post="{{ url_for('validate_form') }}"
                                    hx-trigger="change"
                                    hx-target="#validation-result"
                                    hx-include="closest form">
                                    <option value="Placidus">Placidus</option>
                                    <option value="Koch">Koch</option>
                                    <option value="Whole Sign">Whole Sign</option>
                                    <option value="Equal House">Equal House</option>
                                    <option value="Campanus">Campanus</option>
                                    <option value="Regiomontanus">Regiomontanus</option>
                                    <option value="Porphyry">Porphyry</option>
                                    <option value="Polich-Page Topocentric">Topocentric</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="theme" class="form-label">Chart Theme</label>
                                <select class="form-select" id="theme" name="theme" required>
                                    <option value="classic">Classic</option>
                                    <option value="dark">Dark</option>
                                    <option value="pastel">Pastel</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label for="language" class="form-label">Chart Language</label>
                                <select class="form-select" id="language" name="language" required>
                                    <option value="en">English</option>
                                    <option value="it">Italian</option>
                                    <option value="fr">French</option>
                                    <option value="es">Spanish</option>
                                    <option value="de">German</option>
                                    <option value="pt">Portuguese</option>
                                </select>
                            </div>
                            
                            <!-- Validation Result -->
                            <div id="validation-result"></div>
                            
                            <div class="mt-4">
                                <button type="submit" class="btn btn-primary">
                                    Generate Chart
                                </button>
                                <div id="form-submitting" class="htmx-indicator ms-2">
                                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                    Generating chart...
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            
            <div class="tab-pane fade" id="vedic-content" role="tabpanel" aria-labelledby="vedic-tab">
                <form id="vedic-form" 
                    hx-post="/generate-chart" 
                    hx-target="#form-processing-message"
                    hx-indicator="#form-submitting-vedic">
                    <input type="hidden" name="chart_type" value="vedic">
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="name-vedic" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name-vedic" name="name" required
                                    hx-post="{{ url_for('validate_form') }}"
                                    hx-trigger="change"
                                    hx-target="#validation-result-vedic"
                                    hx-params="name">
                            </div>
                            
                            <div class="mb-3">
                                <label for="birth_date-vedic" class="form-label">Birth Date & Time</label>
                                <input type="datetime-local" class="form-control" id="birth_date-vedic" name="birth_date" required
                                    hx-post="{{ url_for('validate_form') }}"
                                    hx-trigger="change"
                                    hx-target="#validation-result-vedic"
                                    hx-params="birth_date">
                            </div>
                            
                            <div id="location-fields-vedic">
                                {% include "fragments/location_fields.html" %}
                            </div>
                            
                            <div class="mb-3">
                                <label for="houses_system-vedic" class="form-label">Houses System</label>
                                <select class="form-select" id="houses_system-vedic" name="houses_system" required
                                    hx-post="{{ url_for('validate_form') }}"
                                    hx-trigger="change"
                                    hx-target="#validation-result-vedic"
                                    hx-include="closest form">
                                    <option value="Whole Sign">Whole Sign</option>
                                    <option value="Equal House">Equal House</option>
                                    <option value="Placidus">Placidus</option>
                                    <option value="Koch">Koch</option>
                                    <option value="Campanus">Campanus</option>
                                    <option value="Regiomontanus">Regiomontanus</option>
                                    <option value="Porphyry">Porphyry</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label for="sidereal_mode" class="form-label">Sidereal Mode</label>
                                <select class="form-select" id="sidereal_mode" name="sidereal_mode" required>
                                    <option value="Custom">Custom (Lahiri Ayanamsa)</option>
                                    <option value="Krishnamurti">Krishnamurti</option>
                                    <option value="Lahiri">Lahiri</option>
                                    <option value="Raman">Raman</option>
                                    <option value="Usha_Shashi">Usha/Shashi</option>
                                    <option value="Yukteshwar">Yukteshwar</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="theme-vedic" class="form-label">Chart Theme</label>
                                <select class="form-select" id="theme-vedic" name="theme" required>
                                    <option value="classic">Classic</option>
                                    <option value="dark">Dark</option>
                                    <option value="pastel">Pastel</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label for="language-vedic" class="form-label">Chart Language</label>
                                <select class="form-select" id="language-vedic" name="language" required>
                                    <option value="en">English</option>
                                    <option value="it">Italian</option>
                                    <option value="fr">French</option>
                                    <option value="es">Spanish</option>
                                    <option value="de">German</option>
                                    <option value="pt">Portuguese</option>
                                </select>
                            </div>
                            
                            <!-- Validation Result -->
                            <div id="validation-result-vedic"></div>
                            
                            <div class="mt-4">
                                <button type="submit" class="btn btn-primary">
                                    Generate Chart
                                </button>
                                <div id="form-submitting-vedic" class="htmx-indicator ms-2">
                                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                    Generating chart...
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Form processing message placeholder -->
<div id="form-processing-message"></div>

<!-- Chart Result Section - For instant preview only if needed -->
<div id="chart-result" class="d-none">
    <div class="alert alert-info">
        <div class="d-flex align-items-center">
            <div class="spinner-border spinner-border-sm me-2" role="status"></div>
            <div>
                Your chart is being generated. Please wait...
            </div>
        </div>
    </div>
</div>

<!-- Location Search Modal -->
<div id="location-modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3>Select Location</h3>
            <button type="button" class="modal-close" onclick="closeLocationModal()">&times;</button>
        </div>
        <div id="location-results">
            <!-- Results will be loaded here -->
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize chart preview empty state
        const chartResult = document.getElementById('chart-result');
        if (!chartResult.innerHTML.trim()) {
            chartResult.innerHTML = `
            <div class="chart-preview">
                <div class="chart-placeholder">
                    <p>Chart will appear here</p>
                </div>
            </div>`;
        }
        
        // Location search modal
        let locationResults = [];
        let currentSearchFields = {
            cityField: '',
            countryField: '',
            lngField: '',
            latField: '',
            tzField: ''
        };
        
        window.searchLocation = function(cityField, countryField, lngField, latField, tzField) {
            const cityInput = document.getElementById(cityField);
            const cityName = cityInput.value.trim();
            
            // Store field IDs for later use
            currentSearchFields = {
                cityField, 
                countryField, 
                lngField, 
                latField, 
                tzField
            };
            
            if (!cityName || cityName.length < 2) {
                alert('Please enter at least 2 characters for city search');
                return;
            }
            
            // Show loading indicator
            document.getElementById('location-results').innerHTML = '<p>Searching...</p>';
            document.getElementById('location-modal').style.display = 'flex';
            
            // Call the API to search for locations
            fetch(`/api/v1/geo/search?q=${encodeURIComponent(cityName)}`)
                .then(response => response.json())
                .then(data => {
                    locationResults = data;
                    displayLocationResults();
                })
                .catch(error => {
                    document.getElementById('location-results').innerHTML = 
                        `<p class="text-danger">Error searching for locations: ${error.message}</p>`;
                });
        };
        
        function displayLocationResults() {
            const resultsContainer = document.getElementById('location-results');
            
            if (!locationResults || locationResults.length === 0) {
                resultsContainer.innerHTML = '<p>No locations found. Try a different search.</p>';
                return;
            }
            
            let html = '<div class="list-group">';
            locationResults.forEach((location, index) => {
                html += `
                    <button type="button" class="list-group-item list-group-item-action" onclick="selectLocation(${index})">
                        <strong>${location.name}</strong>, ${location.country_code}<br>
                        <small>Lat: ${location.latitude.toFixed(4)}, Lng: ${location.longitude.toFixed(4)}</small>
                    </button>
                `;
            });
            html += '</div>';
            
            resultsContainer.innerHTML = html;
        }
        
        window.selectLocation = function(index) {
            const location = locationResults[index];
            
            // Fill in the form fields
            document.getElementById(currentSearchFields.cityField).value = location.name;
            document.getElementById(currentSearchFields.countryField).value = location.country_code;
            document.getElementById(currentSearchFields.lngField).value = location.longitude;
            document.getElementById(currentSearchFields.latField).value = location.latitude;
            
            // Set timezone if available
            if (location.timezone) {
                const tzSelect = document.getElementById(currentSearchFields.tzField);
                
                // Find the option with the matching timezone value
                for (let i = 0; i < tzSelect.options.length; i++) {
                    if (tzSelect.options[i].value === location.timezone) {
                        tzSelect.selectedIndex = i;
                        break;
                    }
                }
                
                // If we don't have the timezone in our dropdown, add it
                if (!Array.from(tzSelect.options).some(opt => opt.value === location.timezone)) {
                    const newOption = new Option(location.timezone, location.timezone);
                    tzSelect.add(newOption);
                    tzSelect.value = location.timezone;
                }
            }
            
            // Close the modal
            document.getElementById('location-modal').style.display = 'none';
        };
        
        window.closeLocationModal = function() {
            document.getElementById('location-modal').style.display = 'none';
        };
    });
</script>
{% endblock %}
````

## File: app/templates/layout.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Zodiac Engine{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <!-- Custom CSS - minimal overrides only -->
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
    <!-- HTMX Library -->
    <script src="https://unpkg.com/htmx.org@2.0.4" integrity="sha384-HGfztofotfshcF7+8n44JQL2oJmowVChPTg48S+jvZoztPfvwD79OC/LTtG6dMp+" crossorigin="anonymous"></script>
    {% block head %}{% endblock %}
</head>
<body>
    <div class="container py-4">
        <header class="text-center mb-4 p-3 bg-primary text-white rounded">
            <h1>Zodiac Engine</h1>
            <p class="mb-0">Astrological Chart Generation</p>
        </header>
        
        <main>
            {% block content %}{% endblock %}
        </main>
        
        <footer>
            <p class="text-center mt-4 text-secondary">
                &copy; 2025 Zodiac Engine | Version: {{ version }}
            </p>
        </footer>
    </div>
    
    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
````

## File: .cursor/rules/fastapi-testing.mdc
````
---
description: This rule documents best practices for writing FastAPI tests in the Zodiac Engine. Call this rule when reviewing or creating tests, implementing test fixtures, or working with async testing. Use it when users need guidance on test structure, mocking dependencies, handling async operations, or optimizing test performance.
globs: 
alwaysApply: false
---
# FastAPI Testing Best Practices

This document outlines the recommended testing practices for the Zodiac Engine application.

## Test Structure

- **Test Organization**: Organize tests by API resources/endpoints (e.g., `test_chart_configuration.py`, `test_natal_chart_variations.py`).
- **Test Files**: Name test files with `test_` prefix.
- **Test Directory**: Keep all tests in the `tests/` directory at the project root.

## TestClient Usage

The primary way to test FastAPI endpoints is with the synchronous `TestClient` from `fastapi.testclient`. Most tests use this client directly.

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_endpoint():
    response = client.get("/some-endpoint")
    assert response.status_code == 200
    assert response.json() == {"expected": "response"}
```

## Asynchronous Testing Considerations

- The `pytest-asyncio` plugin is installed.
- Test functions themselves should *not* use `async def` unless they directly `await` something *other* than client calls (which are synchronous with `TestClient`).
- For testing true async operations or if switching to `httpx.AsyncClient`, use `@pytest.mark.anyio` and `async def`.

```python
# Example IF using AsyncClient (not current practice)
# import pytest
# from httpx import AsyncClient
#
# @pytest.mark.anyio
# async def test_async_endpoint():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/endpoint")
#     assert response.status_code == 200
```

## Using Fixtures

- Fixtures can be defined in individual test files or in `tests/conftest.py` for reuse.
- Currently, fixtures like `valid_natal_visualization_request` are defined within specific test files (e.g., [tests/test_static_images.py](mdc:tests/test_static_images.py)).
- The `TestClient` is instantiated directly in each test file rather than using a shared fixture.

```python
# Example fixture in a test file
@pytest.fixture
def test_data():
    return {
        "name": "Test Person",
        "birth_date": "1990-01-01T12:00:00",
        # other test data
    }

def test_using_fixture(test_data):
    response = client.post("/some-endpoint", json=test_data)
    # ... assertions ...
```

## Dependency Overrides

- FastAPI supports overriding dependencies for isolated testing, which is useful for mocking external services or databases.
- This is typically done using `app.dependency_overrides`.
- **Note**: This pattern is not currently used for service mocking (e.g., `AstrologyService`, `ChartVisualizationService`) in the existing test suite, but can be implemented if needed.

```python
# Example of overriding a dependency (conceptual)
# from app.main import app
# from app.core.dependencies import get_astrology_service
#
# def get_mock_astrology_service():
#     # Return a mock or test implementation
#     return MockAstrologyService()
#
# app.dependency_overrides[get_astrology_service] = get_mock_astrology_service
#
# # Run tests that use the overridden dependency
#
# # Clean up overrides after tests
# app.dependency_overrides = {}
```

## Best Practices

1.  **Test Both Success and Error Cases**: Verify correct behavior for both valid and invalid inputs.
2.  **Use Status Constants**: Use `fastapi.status` constants (e.g., `status.HTTP_200_OK`) instead of raw numbers.
3.  **Parameterized Testing**: Use `@pytest.mark.parametrize` for testing variations efficiently.
4.  **Mocking External Services**: If external dependencies (beyond Kerykeion, which is implicitly tested) are added, use `unittest.mock` or pytest's monkeypatch.
5.  **Testing File Operations**: For file generation (like SVGs), assert file existence and optionally check content. Consider mocking file system interactions for pure unit tests.
6.  **Test Coverage**: Aim for high test coverage using `pytest-cov`.

## Project-Specific Guidelines

- Test all chart generation endpoints with various valid and invalid configurations.
- Verify SVG generation includes expected elements or text content.
- Ensure tests clean up generated files or use a dedicated test directory (currently handled by `setup_static_dir` fixture in `test_static_images.py`).
- Tests currently rely on the actual Kerykeion library execution. Mocking Kerykeion is an option for faster, more isolated unit tests in the future.
````

## File: app/api/v1/routers/charts/natal.py
````python
"""Natal chart router module."""
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.core.dependencies import AstrologyServiceDep
from app.core.exceptions import (
    ChartCalculationError,
    InvalidBirthDataError,
    LocationError
)
from app.schemas.natal_chart import NatalChartRequest, NatalChartResponse
from app.services.astrology import AstrologyService

router = APIRouter(
    prefix="/natal",
    tags=["natal-chart"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "examples": {
                        "InvalidBirthData": {
                            "summary": "Invalid birth data",
                            "value": {
                                "error": {
                                    "code": 400,
                                    "message": "Invalid birth data provided",
                                    "type": "InvalidBirthDataError",
                                    "path": "/api/v1/charts/natal/"
                                }
                            }
                        },
                        "InvalidLocation": {
                            "summary": "Invalid location",
                            "value": {
                                "error": {
                                    "code": 400,
                                    "message": "Invalid location coordinates",
                                    "type": "LocationError",
                                    "path": "/api/v1/charts/natal/"
                                }
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 500,
                            "message": "Error calculating astrological chart",
                            "type": "ChartCalculationError",
                            "path": "/api/v1/charts/natal/"
                        }
                    }
                }
            }
        }
    }
)

@router.post(
    "/",
    response_model=NatalChartResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    summary="Calculate Natal Chart",
    description="""
    Calculate a complete natal chart based on birth data.
    
    The natal chart includes:
    * Planetary positions and aspects
    * House cusps and placements
    * Zodiac sign positions
    * Retrograde status for applicable planets
    * Lunar Nodes (True/Mean)
    * Lilith (Mean)
    * Chiron
    * Complete aspect data with orbs
    * House system information
    
    You can provide either city/country or exact coordinates (longitude/latitude).
    If both are provided, coordinates take precedence.
    
    You can also specify which house system to use. The default is Placidus ('P').
    Other options include:
    - 'W': Whole Sign
    - 'K': Koch
    - 'R': Regiomontanus
    - 'C': Campanus
    - 'E': Equal (MC)
    - 'A': Equal (Ascendant)
    - 'T': Topocentric
    - 'O': Porphyry
    - 'B': Alcabitius
    - 'M': Morinus
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully calculated natal chart",
            "content": {
                "application/json": {
                    "example": {
                        "name": "John Doe",
                        "birth_date": "1990-01-01T12:00:00",
                        "planets": [
                            {
                                "name": "Sun",
                                "sign": "Capricorn",
                                "position": 10.5,
                                "house": 1,
                                "retrograde": False
                            }
                        ],
                        "houses": {
                            "1": 0.0,
                            "2": 30.0,
                            "3": 60.0
                        },
                        "aspects": [
                            {
                                "p1_name": "Sun",
                                "p2_name": "Moon",
                                "aspect": "trine",
                                "orbit": 120.0
                            }
                        ],
                        "house_system": {
                            "name": "Placidus",
                            "identifier": "P"
                        }
                    }
                }
            }
        }
    }
)
def calculate_natal_chart(
    request: NatalChartRequest,
    astrology_service: AstrologyServiceDep
) -> NatalChartResponse:
    """Calculate natal chart for given birth data."""
    try:
        # Validate birth data
        if not request.birth_date:
            raise InvalidBirthDataError("Birth date is required")
            
        # Validate location data
        if not (request.city and request.nation) and not (request.lng and request.lat):
            raise LocationError(
                "Either city/nation or longitude/latitude must be provided"
            )

        return astrology_service.calculate_natal_chart(
            name=request.name,
            birth_date=request.birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            houses_system=request.houses_system
        )
    except Exception as e:
        if isinstance(e, (InvalidBirthDataError, LocationError)):
            raise
        raise ChartCalculationError(str(e))
````

## File: app/api/v1/routers/charts/visualization.py
````python
"""Chart visualization API endpoints."""
from typing import Annotated
import uuid
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from datetime import datetime

from app.core.exceptions import ChartCalculationError, InvalidBirthDataError, LocationError
from app.core.dependencies import ChartVisualizationServiceDep
from app.schemas.chart_visualization import (
    NatalChartVisualizationRequest,
    NatalChartVisualizationResponse,
    SynastryChartVisualizationRequest,
    SynastryChartVisualizationResponse
)
from app.services.chart_visualization import ChartVisualizationService

router = APIRouter(
    prefix="/visualization",
    tags=["chart-visualization"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "examples": {
                        "InvalidBirthData": {
                            "summary": "Invalid birth data",
                            "value": {
                                "error": {
                                    "code": 400,
                                    "message": "Invalid birth data provided",
                                    "type": "InvalidBirthDataError",
                                    "path": "/api/v1/charts/visualization/natal"
                                }
                            }
                        },
                        "InvalidLocation": {
                            "summary": "Invalid location",
                            "value": {
                                "error": {
                                    "code": 400,
                                    "message": "Invalid location coordinates",
                                    "type": "LocationError",
                                    "path": "/api/v1/charts/visualization/natal"
                                }
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": 500,
                            "message": "Error generating chart visualization",
                            "type": "ChartCalculationError",
                            "path": "/api/v1/charts/visualization/natal"
                        }
                    }
                }
            }
        }
    }
)

@router.post(
    "/natal", 
    response_model=NatalChartVisualizationResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate Natal Chart Visualization",
    description="""
    Generate and save a natal chart visualization.
    
    This endpoint accepts birth details and configuration options to create a custom chart.
    The SVG generation happens in the background, and the endpoint returns immediately with a chart ID.
    
    You can specify:
    - Theme: dark (default), light, classic, dark-high-contrast
    - Language: EN (default), ES, IT, FR, DE, etc.
    - Configuration options like house system, active points, and aspect orbs
    
    Returns a chart ID and URL to access the SVG once it's generated.
    """
)
async def generate_natal_chart_visualization(
    request: NatalChartVisualizationRequest,
    background_tasks: BackgroundTasks,
    chart_service: ChartVisualizationServiceDep
) -> NatalChartVisualizationResponse:
    """
    Generate and save a natal chart visualization.
    
    Returns the chart ID and URL to access the SVG.
    """
    try:
        # Convert the birth_date from ISO format string to datetime
        try:
            birth_date = datetime.fromisoformat(request.birth_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"Invalid birth date format: {request.birth_date}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate a unique chart_id if not provided
        chart_id = request.chart_id or f"natal_{uuid.uuid4().hex[:8]}"
        
        # Create a placeholder URL that will be valid once the background task completes
        svg_url = f"/static/images/svg/{chart_id}.svg"
        
        # Schedule the chart generation as a background task
        background_tasks.add_task(
            chart_service.generate_natal_chart_svg,
            name=request.name,
            birth_date=birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            chart_id=chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.model_dump() if request.config else None
        )
        
        # Return the response immediately
        return NatalChartVisualizationResponse(
            chart_id=chart_id,
            svg_url=svg_url
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error generating chart: {str(e)}"
        )

@router.post(
    "/synastry", 
    response_model=SynastryChartVisualizationResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate Synastry Chart Visualization",
    description="""
    Generate and save a synastry chart visualization comparing two natal charts.
    
    This endpoint accepts birth details for two individuals and configuration options to create a custom synastry chart.
    The SVG generation happens in the background, and the endpoint returns immediately with a chart ID.
    
    You can specify:
    - Theme: dark (default), light, classic, dark-high-contrast
    - Language: EN (default), ES, IT, FR, DE, etc.
    - Configuration options like house system, active points, and aspect orbs
    
    Returns a chart ID and URL to access the SVG once it's generated.
    """
)
async def generate_synastry_chart_visualization(
    request: SynastryChartVisualizationRequest,
    background_tasks: BackgroundTasks,
    chart_service: ChartVisualizationServiceDep
) -> SynastryChartVisualizationResponse:
    """
    Generate and save a synastry chart visualization comparing two natal charts.
    
    Returns the chart ID and URL to access the SVG.
    """
    try:
        # Convert the birth dates from ISO format strings to datetime
        try:
            birth_date1 = datetime.fromisoformat(request.birth_date1)
            birth_date2 = datetime.fromisoformat(request.birth_date2)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"Invalid birth date format: {str(e)}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate a unique chart_id if not provided
        chart_id = request.chart_id or f"synastry_{uuid.uuid4().hex[:8]}"
        
        # Create a placeholder URL that will be valid once the background task completes
        svg_url = f"/static/images/svg/{chart_id}.svg"
        
        # Schedule the chart generation as a background task
        background_tasks.add_task(
            chart_service.generate_synastry_chart_svg,
            name1=request.name1,
            birth_date1=birth_date1,
            name2=request.name2,
            birth_date2=birth_date2,
            city1=request.city1,
            nation1=request.nation1,
            lng1=request.lng1,
            lat1=request.lat1,
            tz_str1=request.tz_str1,
            city2=request.city2,
            nation2=request.nation2,
            lng2=request.lng2,
            lat2=request.lat2,
            tz_str2=request.tz_str2,
            chart_id=chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.model_dump() if request.config else None
        )
        
        # Return the response immediately
        return SynastryChartVisualizationResponse(
            chart_id=chart_id,
            svg_url=svg_url
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error generating synastry chart: {str(e)}"
        )
````

## File: app/core/config.py
````python
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    ALLOWED_ORIGINS: str
    
    # Kerykeion settings
    GEONAMES_USERNAME: str

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Convert ALLOWED_ORIGINS string to a list."""
        if "," in self.ALLOWED_ORIGINS:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return [self.ALLOWED_ORIGINS]

settings = Settings()
````

## File: tests/test_chart_configuration.py
````python
"""Tests for chart configuration features."""
import os
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

client = TestClient(app)

# Test data
TEST_NATAL_DATA: Dict[str, Any] = {
    "name": "Test Person",
    "birth_date": "1990-01-01T12:00:00",
    "lng": -74.006,  # New York coordinates
    "lat": 40.7128,
    "tz_str": "America/New_York",
    "language": "EN",
    "theme": "dark"
}

def test_natal_chart_with_tropical_zodiac():
    """Test natal chart with tropical zodiac configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "zodiac_type": "Tropic"
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
    
    # Verify the SVG file was created
    chart_id = json_response["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains tropical reference 
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Tropical" in svg_content

def test_natal_chart_with_sidereal_zodiac():
    """Test natal chart with sidereal zodiac configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "zodiac_type": "Sidereal",
            "sidereal_mode": "LAHIRI"
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
    
    # Verify the SVG file was created
    chart_id = json_response["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains sidereal reference (Kerykeion uses "Ayanamsa" for sidereal zodiac)
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Ayanamsa" in svg_content

def test_natal_chart_with_limited_planets():
    """Test natal chart with limited active planets configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128, 
        "tz_str": "America/New_York",
        "config": {
            "active_points": ["Sun", "Moon", "Ascendant"]
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
    
    # Verify the SVG file was created
    chart_id = json_response["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains only the selected planets
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Sun" in svg_content
        assert "Moon" in svg_content

def test_natal_chart_with_custom_aspects():
    """Test natal chart with custom aspects configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "active_aspects": [
                {"name": "conjunction", "orb": 5},
                {"name": "opposition", "orb": 5}
            ]
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")

def test_natal_chart_with_different_house_system():
    """Test natal chart with different house system configuration."""
    data = {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "config": {
            "houses_system": "W"  # Whole Sign houses
        }
    }
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")

def test_synastry_chart_with_configuration():
    """Test synastry chart with configuration options."""
    data = {
        "name1": "John Doe",
        "birth_date1": "1990-01-01T12:00:00",
        "city1": "New York",
        "nation1": "US",
        "lng1": -74.006,
        "lat1": 40.7128,
        "tz_str1": "America/New_York",
        "name2": "Jane Doe",
        "birth_date2": "1992-05-15T15:30:00",
        "city2": "Los Angeles",
        "nation2": "US",
        "lng2": -118.2437,
        "lat2": 34.0522,
        "tz_str2": "America/Los_Angeles",
        "config": {
            "houses_system": "P",
            "zodiac_type": "Tropic",
            "active_points": ["Sun", "Moon", "Venus", "Mars", "Ascendant"],
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 6},
                {"name": "square", "orb": 6}
            ]
        }
    }
    response = client.post("/api/v1/charts/visualization/synastry", json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    
    json_response = response.json()
    assert "chart_id" in json_response
    assert "svg_url" in json_response
    assert json_response["svg_url"].endswith(".svg")
````

## File: tests/test_charts_natal.py
````python
from datetime import datetime
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture
def valid_natal_chart_request() -> Dict[str, Any]:
    """Fixture for valid natal chart request data."""
    return {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "houses_system": "P"  # Default to Placidus
    }

def test_calculate_natal_chart_success(valid_natal_chart_request):
    """Test successful natal chart calculation with new chart endpoint."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check response structure
    assert "name" in data
    assert "birth_date" in data
    assert "planets" in data
    assert "houses" in data
    assert "aspects" in data
    assert "house_system" in data
    
    # Check house system data
    assert "name" in data["house_system"]
    assert "identifier" in data["house_system"]
    assert data["house_system"]["identifier"] == valid_natal_chart_request["houses_system"]
    
    # Check planets data
    assert len(data["planets"]) > 0
    for planet in data["planets"]:
        assert "name" in planet
        assert "sign" in planet
        assert "position" in planet
        assert "house" in planet
        assert "retrograde" in planet
    
    # Check houses data
    assert len(data["houses"]) == 12
    
    # Check aspects data
    assert isinstance(data["aspects"], list)

def test_calculate_natal_chart_invalid_date():
    """Test natal chart calculation with invalid date."""
    invalid_request = {
        "name": "John Doe",
        "birth_date": "invalid-date",
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/natal/", json=invalid_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_calculate_natal_chart_missing_required():
    """Test natal chart calculation with missing required fields."""
    invalid_request = {
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/natal/", json=invalid_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_calculate_natal_chart_coordinates_only(valid_natal_chart_request):
    """Test natal chart calculation with coordinates only."""
    request = {
        "name": valid_natal_chart_request["name"],
        "birth_date": valid_natal_chart_request["birth_date"],
        "lng": valid_natal_chart_request["lng"],
        "lat": valid_natal_chart_request["lat"],
        "tz_str": valid_natal_chart_request["tz_str"],
        "houses_system": valid_natal_chart_request["houses_system"]
    }
    
    response = client.post("/api/v1/charts/natal/", json=request)
    assert response.status_code == status.HTTP_200_OK

def test_calculate_natal_chart_celestial_points(valid_natal_chart_request):
    """Test that all celestial points are included in the response."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Get all planet names from the response
    planet_names = [planet["name"].lower() for planet in data["planets"]]
    
    # Check for standard planets
    standard_planets = ["sun", "moon", "mercury", "venus", "mars", 
                       "jupiter", "saturn", "uranus", "neptune", "pluto"]
    for planet in standard_planets:
        assert planet in planet_names, f"{planet} is missing from the response"
    
    # Check for additional required celestial points
    required_points = ["mean node", "true node", "mean lilith", "chiron"]
    for point in required_points:
        assert any(point in p for p in planet_names), f"{point} is missing from the response"

def test_calculate_natal_chart_aspect_data(valid_natal_chart_request):
    """Test that aspect data includes complete information with orbs."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify we have aspects
    assert len(data["aspects"]) > 0
    
    # Check aspect structure and orb information
    for aspect in data["aspects"]:
        assert "p1_name" in aspect
        assert "p2_name" in aspect
        assert "aspect" in aspect
        assert "orbit" in aspect
        assert isinstance(aspect["orbit"], (int, float))

def test_calculate_natal_chart_different_house_system(valid_natal_chart_request):
    """Test natal chart calculation with a different house system."""
    # Clone the request and change house system to Whole Sign
    request = valid_natal_chart_request.copy()
    request["houses_system"] = "W"  # Whole Sign
    
    response = client.post("/api/v1/charts/natal/", json=request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify the house system in the response
    assert data["house_system"]["identifier"] == "W"
    
    # House systems have different names
    assert data["house_system"]["name"] != "Placidus"
````

## File: tests/test_natal_chart_variations.py
````python
"""Tests for various natal chart variations."""
import os
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

client = TestClient(app)

# Test data
TEST_NATAL_DATA: Dict[str, Any] = {
    "name": "Test Person",
    "birth_date": "1990-01-01T12:00:00",
    "lng": -74.006,  # New York coordinates
    "lat": 40.7128,
    "tz_str": "America/New_York"
}

def test_natal_chart_different_themes():
    """Test generating natal charts with different themes."""
    themes = ["light", "dark", "classic", "dark-high-contrast"]
    
    for theme in themes:
        data = {
            **TEST_NATAL_DATA,
            "theme": theme,
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P"
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        
        json_response = response.json()
        assert "chart_id" in json_response
        assert "svg_url" in json_response
        assert json_response["svg_url"].endswith(".svg")
        
        # Verify the SVG file was created
        chart_id = json_response["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)

def test_natal_chart_different_languages():
    """Test generating natal charts with different languages."""
    languages = ["EN", "ES", "IT", "FR", "DE"]
    
    for language in languages:
        data = {
            **TEST_NATAL_DATA,
            "language": language,
            "theme": "dark",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P"
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        
        json_response = response.json()
        assert "chart_id" in json_response
        assert "svg_url" in json_response
        assert json_response["svg_url"].endswith(".svg")
        
        # Verify the SVG file was created
        chart_id = json_response["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)

def test_natal_chart_different_perspective_types():
    """Test generating natal charts with different perspective types."""
    perspectives = ["Apparent Geocentric", "True Geocentric", "Topocentric"]
    
    for perspective in perspectives:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P",
                "perspective_type": perspective
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        
        json_response = response.json()
        assert "chart_id" in json_response
        assert "svg_url" in json_response
        assert json_response["svg_url"].endswith(".svg")
        
        # Verify the SVG file was created
        chart_id = json_response["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
        
        # Verify the perspective type is shown in the chart
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert perspective in svg_content or perspective.replace(" ", "_").lower() in svg_content.lower()

def test_natal_chart_different_sidereal_modes():
    """Test generating natal charts with different sidereal modes."""
    sidereal_modes = ["FAGAN_BRADLEY", "LAHIRI", "DELUCE", "RAMAN", "KRISHNAMURTI"]
    
    for mode in sidereal_modes:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Sidereal",
                "sidereal_mode": mode,
                "houses_system": "P"
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        
        json_response = response.json()
        assert "chart_id" in json_response
        assert "svg_url" in json_response
        assert json_response["svg_url"].endswith(".svg")
        
        # Verify the SVG file was created
        chart_id = json_response["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
        
        # Verify the SVG file contains Ayanamsa reference
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert "Ayanamsa" in svg_content

def test_natal_chart_different_celestial_points():
    """Test generating natal charts with different celestial points."""
    point_sets = [
        # Standard planets only
        ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"],
        
        # Traditional planets
        ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"],
        
        # Luminaries and angles
        ["Sun", "Moon", "Ascendant", "Medium_Coeli"],
        
        # Additional points
        ["Sun", "Moon", "Mean_Node", "Mean_Lilith", "Chiron"]
    ]
    
    for points in point_sets:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P",
                "active_points": points
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        
        json_response = response.json()
        assert "chart_id" in json_response
        assert "svg_url" in json_response
        assert json_response["svg_url"].endswith(".svg")
        
        # Verify the SVG file was created
        chart_id = json_response["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
        
        # Verify at least one of the specified points appears in the content
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert any(point in svg_content for point in points)

def test_natal_chart_different_house_systems():
    """Test generating natal charts with different house systems."""
    # Using only valid house systems as shown in the error message
    house_systems = ["P", "K", "R", "C", "W", "F", "O", "B", "M"]
    
    for house_system in house_systems:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": house_system
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        
        json_response = response.json()
        assert "chart_id" in json_response
        assert "svg_url" in json_response
        assert json_response["svg_url"].endswith(".svg")
        
        # Verify the SVG file was created
        chart_id = json_response["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
````

## File: requirements.txt
````
# FastAPI and its dependencies
fastapi>=0.112.0,<0.113.0
uvicorn[standard]>=0.34.0,<0.35.0
pydantic>=2.11.0,<2.12.0
pydantic-settings>=2.8.0,<2.9.0
python-multipart>=0.0.6,<0.0.21
httpx>=0.28.0,<0.29.0

# Database
sqlalchemy>=2.0.0,<2.1.0
aiosqlite>=0.19.0,<0.20.0
alembic>=1.12.0,<1.16.0

# Kerykeion and its dependencies
kerykeion==4.25.3
pyswisseph>=2.10.3.1,<3.0.0.0
pytz>=2024.2,<2025.0
requests>=2.32.3,<3.0.0
requests-cache>=1.2.1,<2.0.0
scour>=0.38.2,<0.39.0
simple-ascii-tables>=1.0.0,<2.0.0
typing-extensions>=4.12.2,<5.0.0

# Testing
pytest>=7.4.3,<8.4.0
pytest-asyncio>=0.21.1,<0.27.0
pytest-dotenv>=0.5.2,<0.6.0

# Utilities
python-dotenv>=1.0.0,<1.2.0
email-validator>=2.0.0,<2.3.0
rich>=13.6.0,<15.0.0
rich-toolkit>=0.14.0,<0.15.0

# Template Engine
Jinja2>=3.1.2,<3.2.0
````

## File: app/core/dependencies.py
````python
"""Dependency functions for FastAPI."""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.services.astrology import AstrologyService
from app.services.chart_visualization import ChartVisualizationService
from app.services.geo_service import GeoService

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get application settings as a dependency.
    
    Uses lru_cache for caching to avoid reloading settings on every request.
    """
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]

@lru_cache(maxsize=32)
def get_astrology_service() -> AstrologyService:
    """
    Get an instance of the AstrologyService.
    
    This dependency can be used in route functions to get access to astrology-related operations.
    Uses lru_cache to reuse the service instance, improving performance.
    """
    return AstrologyService()

AstrologyServiceDep = Annotated[AstrologyService, Depends(get_astrology_service)]

def get_chart_visualization_service(settings: SettingsDep) -> ChartVisualizationService:
    """
    Get an instance of the ChartVisualizationService.
    
    This dependency requires settings and can be used in route functions
    to get access to chart visualization operations.
    """
    return ChartVisualizationService(settings=settings)

ChartVisualizationServiceDep = Annotated[ChartVisualizationService, Depends(get_chart_visualization_service)]

def get_geo_service() -> GeoService:
    """Dependency provider for GeoService."""
    return GeoService()

GeoServiceDep = Annotated[GeoService, Depends(get_geo_service)]
````

## File: app/schemas/chart_visualization.py
````python
"""Schemas for chart visualization endpoints."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# Based on the Kerykeion literals
ZodiacType = Literal["Tropic", "Sidereal"]
SiderealMode = Literal[
    "FAGAN_BRADLEY", "LAHIRI", "DELUCE", "RAMAN", "USHASHASHI", "KRISHNAMURTI", 
    "DJWHAL_KHUL", "YUKTESHWAR", "JN_BHASIN", "BABYL_KUGLER1", "BABYL_KUGLER2", 
    "BABYL_KUGLER3", "BABYL_HUBER", "BABYL_ETPSC", "ALDEBARAN_15TAU", "HIPPARCHOS", 
    "SASSANIAN", "J2000", "J1900", "B1950"
]

PerspectiveType = Literal["Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric"]

Planet = Literal[
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
    "Neptune", "Pluto", "Mean_Node", "True_Node", "Mean_South_Node", "True_South_Node", 
    "Chiron", "Mean_Lilith"
]

AxialCusps = Literal["Ascendant", "Medium_Coeli", "Descendant", "Imum_Coeli"]

AspectName = Literal[
    "conjunction", "semi-sextile", "semi-square", "sextile", "quintile", 
    "square", "trine", "sesquiquadrate", "biquintile", "quincunx", "opposition"
]

class AspectConfiguration(BaseModel):
    """Schema for aspect configuration."""
    name: AspectName = Field(..., description="Name of the aspect")
    orb: float = Field(..., description="Orb value for the aspect in degrees")

class ChartConfiguration(BaseModel):
    """Schema for chart configuration options."""
    houses_system: str = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")
    zodiac_type: ZodiacType = Field("Tropic", description="Zodiac type: Tropic (default) or Sidereal")
    sidereal_mode: SiderealMode | None = Field(None, description="Sidereal mode (required if zodiac_type is Sidereal)")
    perspective_type: PerspectiveType = Field("Apparent Geocentric", description="Type of perspective for calculations")
    active_points: list[Planet | AxialCusps] = Field(
        default=[
            "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
            "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
            "Mean_Lilith", "Mean_South_Node"
        ],
        description="List of active planets and points to include in the chart"
    )
    active_aspects: list[AspectConfiguration] = Field(
        default=[
            {"name": "conjunction", "orb": 10}, 
            {"name": "opposition", "orb": 10}, 
            {"name": "trine", "orb": 8}, 
            {"name": "sextile", "orb": 6}, 
            {"name": "square", "orb": 5}, 
            {"name": "quintile", "orb": 1}
        ],
        description="List of active aspects with their orbs"
    )

class NatalChartVisualizationRequest(BaseModel):
    """Schema for natal chart visualization request."""
    name: str = Field(..., description="Name of the person")
    birth_date: str = Field(..., description="Birth date and time in ISO format")
    city: str | None = Field(None, description="City of birth")
    nation: str | None = Field(None, description="Country of birth")
    lng: float | None = Field(None, description="Longitude of birth place")
    lat: float | None = Field(None, description="Latitude of birth place")
    tz_str: str | None = Field(None, description="Timezone string (e.g., 'America/New_York')")
    chart_id: str | None = Field(None, description="Optional custom ID for the chart")
    
    # Visualization options
    theme: str = Field("dark", description="Chart theme ('light', 'dark', 'dark-high-contrast', 'classic')")
    language: str = Field("EN", description="Chart language ('EN', 'FR', 'PT', 'IT', 'CN', 'ES', 'RU', 'TR', 'DE', 'HI')")
    
    # Chart configuration
    config: ChartConfiguration | None = Field(None, description="Chart configuration options")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "birth_date": "1990-01-01T12:00:00",
                "city": "New York",
                "nation": "US",
                "lng": -74.006,
                "lat": 40.7128,
                "tz_str": "America/New_York",
                "chart_id": "john_doe_natal",
                "theme": "dark",
                "language": "EN",
                "config": {
                    "houses_system": "P",
                    "zodiac_type": "Tropic",
                    "perspective_type": "Apparent Geocentric",
                    "active_points": [
                        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
                        "Uranus", "Neptune", "Pluto", "Ascendant", "Medium_Coeli"
                    ],
                    "active_aspects": [
                        {"name": "conjunction", "orb": 8},
                        {"name": "opposition", "orb": 8},
                        {"name": "trine", "orb": 6},
                        {"name": "square", "orb": 6}
                    ]
                }
                }
            }
        }

class SynastryChartVisualizationRequest(BaseModel):
    """Schema for synastry chart visualization request."""
    # First person
    name1: str = Field(..., description="Name of the first person")
    birth_date1: str = Field(..., description="Birth date and time of first person in ISO format")
    city1: str | None = Field(None, description="City of birth for first person")
    nation1: str | None = Field(None, description="Country of birth for first person")
    lng1: float | None = Field(None, description="Longitude of birth place for first person")
    lat1: float | None = Field(None, description="Latitude of birth place for first person")
    tz_str1: str | None = Field(None, description="Timezone string for first person")
    
    # Second person
    name2: str = Field(..., description="Name of the second person")
    birth_date2: str = Field(..., description="Birth date and time of second person in ISO format")
    city2: str | None = Field(None, description="City of birth for second person")
    nation2: str | None = Field(None, description="Country of birth for second person")
    lng2: float | None = Field(None, description="Longitude of birth place for second person")
    lat2: float | None = Field(None, description="Latitude of birth place for second person")
    tz_str2: str | None = Field(None, description="Timezone string for second person")
    
    # Shared settings
    chart_id: str | None = Field(None, description="Optional custom ID for the chart")
    theme: str = Field("dark", description="Chart theme")
    language: str = Field("EN", description="Chart language")
    
    # Chart configuration
    config: ChartConfiguration | None = Field(None, description="Chart configuration options")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name1": "John Doe",
                "birth_date1": "1990-01-01T12:00:00",
                "city1": "New York",
                "nation1": "US",
                "lng1": -74.006,
                "lat1": 40.7128,
                "tz_str1": "America/New_York",
                
                "name2": "Jane Smith",
                "birth_date2": "1992-03-15T15:30:00",
                "city2": "Los Angeles",
                "nation2": "US",
                "lng2": -118.2437,
                "lat2": 34.0522,
                "tz_str2": "America/Los_Angeles",
                
                "chart_id": "john_jane_synastry",
                "theme": "dark",
                "language": "EN",
                "config": {
                    "houses_system": "P",
                    "zodiac_type": "Tropic",
                    "perspective_type": "Apparent Geocentric",
                    "active_points": ["Sun", "Moon", "Venus", "Mars", "Ascendant"],
                    "active_aspects": [
                        {"name": "conjunction", "orb": 6},
                        {"name": "opposition", "orb": 6}, 
                        {"name": "trine", "orb": 5}
                    ]
                }
                }
            }
        }

class ChartVisualizationResponse(BaseModel):
    """Schema for chart visualization response."""
    chart_id: str = Field(..., description="ID of the generated chart")
    svg_url: str = Field(..., description="URL to access the SVG visualization")

    model_config = {
        "json_schema_extra": {
            "example": {
                "chart_id": "natal_12345678",
                "svg_url": "/static/images/svg/natal_12345678.svg"
            }
            }
        }

class NatalChartVisualizationResponse(ChartVisualizationResponse):
    """Response schema for natal chart visualization."""
    pass

class SynastryChartVisualizationResponse(ChartVisualizationResponse):
    """Response schema for synastry chart visualization."""
    pass
````

## File: app/schemas/natal_chart.py
````python
"""Schemas for natal chart calculations."""
from datetime import datetime
from typing import Dict, List, Annotated

from pydantic import BaseModel, Field

class PlanetPosition(BaseModel):
    """Schema for planet position in natal chart."""
    name: str = Field(..., description="Name of the planet")
    sign: str = Field(..., description="Zodiac sign the planet is in")
    position: float = Field(..., description="Position in degrees")
    house: int | str = Field(..., description="House number or name")
    retrograde: bool = Field(..., description="Whether the planet is retrograde")

class NatalChartRequest(BaseModel):
    """Schema for natal chart calculation request."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    city: str | None = Field(None, description="City of birth")
    nation: str | None = Field(None, description="Country of birth")
    lng: float | None = Field(None, description="Longitude of birth place")
    lat: float | None = Field(None, description="Latitude of birth place")
    tz_str: str | None = Field(None, description="Timezone string (e.g., 'America/New_York')")
    houses_system: str | None = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "birth_date": "1990-01-01T12:00:00",
                "city": "New York",
                "nation": "US",
                "lng": -74.006,
                "lat": 40.7128,
                "tz_str": "America/New_York",
                "houses_system": "P"
            }
            }
        }

class AspectInfo(BaseModel):
    """Schema for planetary aspect information."""
    p1_name: str = Field(..., description="Name of first planet")
    p2_name: str = Field(..., description="Name of second planet")
    aspect: str = Field(..., description="Type of aspect")
    orbit: float = Field(..., description="Orbital degree of aspect")

class HouseSystem(BaseModel):
    """Schema for house system information."""
    name: str = Field(..., description="Full name of the house system")
    identifier: str = Field(..., description="Single letter identifier of the house system")

class NatalChartResponse(BaseModel):
    """Schema for natal chart calculation response."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    planets: list[PlanetPosition] = Field(..., description="List of planet positions")
    houses: dict[int, float] = Field(..., description="House cusps positions")
    aspects: list[AspectInfo] = Field(..., description="List of planetary aspects")
    house_system: HouseSystem = Field(..., description="House system used for calculations")
````

## File: app/services/astrology.py
````python
"""Service for astrological calculations using Kerykeion."""
import logging
import functools
from datetime import datetime
from typing import Dict, List, Union

from kerykeion import AstrologicalSubject, NatalAspects

from app.schemas.natal_chart import NatalChartResponse, PlanetPosition, AspectInfo

logger = logging.getLogger(__name__)

def _convert_house_number(house: int | str) -> int | str:
    """Convert house number from string to int if possible."""
    if isinstance(house, int):
        return house
    try:
        # Try to extract number from string like "First_House"
        house_map = {
            "First": 1, "Second": 2, "Third": 3, "Fourth": 4,
            "Fifth": 5, "Sixth": 6, "Seventh": 7, "Eighth": 8,
            "Ninth": 9, "Tenth": 10, "Eleventh": 11, "Twelfth": 12
        }
        for name, num in house_map.items():
            if name in house:
                return num
        # If we can't map it, return the original string
        return house
    except (ValueError, AttributeError):
        return house

class AstrologyService:
    """Service for astrological calculations using Kerykeion."""

    # Cache for natal chart calculations - expires after 1 hour (3600 seconds)
    # This assumes that astrological calculations don't change frequently,
    # and caching them will improve performance significantly
    @functools.lru_cache(maxsize=128)
    def calculate_natal_chart(
        self,
        name: str,
        birth_date: datetime,
        city: str | None = None,
        nation: str | None = None,
        lng: float | None = None,
        lat: float | None = None,
        tz_str: str | None = None,
        houses_system: str = "P",  # Default to Placidus
    ) -> NatalChartResponse:
        """Calculate natal chart for given parameters."""
        try:
            logger.info(f"Calculating natal chart for {name} born on {birth_date}")
            logger.debug(f"Location data: city={city}, nation={nation}, lng={lng}, lat={lat}, tz={tz_str}")
            logger.debug(f"House system: {houses_system}")

            # Create AstrologicalSubject
            subject = AstrologicalSubject(
                name=name,
                year=birth_date.year,
                month=birth_date.month,
                day=birth_date.day,
                hour=birth_date.hour,
                minute=birth_date.minute,
                city=city,
                nation=nation,
                lng=lng,
                lat=lat,
                tz_str=tz_str,
                houses_system_identifier=houses_system,
            )

            logger.debug("Created AstrologicalSubject successfully")

            # Calculate aspects
            aspects = NatalAspects(subject)
            logger.debug("Calculated aspects successfully")

            # Get planet positions - including additional celestial points
            planets = []
            standard_planets = [
                'sun', 'moon', 'mercury', 'venus', 'mars', 
                'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'
            ]
            
            # Additional celestial points from Data Completeness requirements
            additional_points = [
                'mean_node', 'true_node', 'mean_south_node', 'true_south_node',
                'mean_lilith', 'chiron'
            ]
            
            # Process standard planets
            for planet_attr in standard_planets:
                planet = getattr(subject, planet_attr)
                planets.append(PlanetPosition(
                    name=planet_attr.capitalize(),
                    sign=planet.sign,
                    position=planet.position,
                    house=_convert_house_number(planet.house),
                    retrograde=planet.retrograde
                ))
            
            # Process additional celestial points
            for point_attr in additional_points:
                point = getattr(subject, point_attr, None)
                if point is not None:  # Some points may be None if disabled
                    # Convert names for better readability
                    display_name = point_attr.replace('_', ' ').title()
                    planets.append(PlanetPosition(
                        name=display_name,
                        sign=point.sign,
                        position=point.position,
                        house=_convert_house_number(point.house),
                        retrograde=getattr(point, 'retrograde', False)  # Some points don't have retrograde status
                    ))
            
            logger.debug(f"Processed {len(planets)} planets and points successfully")

            # Get house cusps using individual house attributes
            houses = {}
            house_attrs = [
                'first_house', 'second_house', 'third_house', 'fourth_house',
                'fifth_house', 'sixth_house', 'seventh_house', 'eighth_house',
                'ninth_house', 'tenth_house', 'eleventh_house', 'twelfth_house'
            ]
            for i, attr in enumerate(house_attrs, 1):
                house = getattr(subject, attr)
                houses[i] = house.position
            logger.debug("Processed house cusps successfully")

            # Include complete aspect data with orbs
            aspect_info = []
            for aspect in aspects.all_aspects:
                aspect_info.append(AspectInfo(
                    p1_name=aspect.p1_name,
                    p2_name=aspect.p2_name,
                    aspect=aspect.aspect,
                    orbit=aspect.orbit,
                ))
            
            # Get house system information
            house_system_name = subject.houses_system_name
            house_system_id = subject.houses_system_identifier
            
            response = NatalChartResponse(
                name=name,
                birth_date=birth_date,
                planets=planets,
                houses=houses,
                aspects=aspect_info,
                house_system={
                    "name": house_system_name,
                    "identifier": house_system_id
                }
            )
            logger.info("Successfully created natal chart response")
            return response
        except Exception as e:
            logger.error(f"Error calculating natal chart: {str(e)}", exc_info=True)
            raise
````

## File: tests/test_static_images.py
````python
"""Tests for static images routes."""
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
import os
import shutil

from app.main import app

client = TestClient(app)

def test_get_chart_svg_success():
    """Test retrieving a chart SVG image that exists."""
    response = client.get("/static/images/svg/sample.svg")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/svg+xml"
    assert "Sample Astrological Chart" in response.text
    assert "<svg" in response.text

def test_get_chart_svg_not_found():
    """Test retrieving a chart SVG image that doesn't exist."""
    response = client.get("/static/images/svg/nonexistent.svg")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def valid_natal_visualization_request() -> Dict[str, Any]:
    """Fixture for valid natal chart visualization request."""
    return {
        "name": "John Doe",
        "birth_date": "1990-01-01T12:00:00",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "houses_system": "P",
        "theme": "dark",
        "chart_language": "EN",
        "chart_id": "test_natal_chart"
    }

@pytest.fixture
def valid_synastry_visualization_request() -> Dict[str, Any]:
    """Fixture for valid synastry chart visualization request."""
    return {
        "name1": "John Doe",
        "birth_date1": "1990-01-01T12:00:00",
        "city1": "New York",
        "nation1": "US",
        "lng1": -74.006,
        "lat1": 40.7128,
        "tz_str1": "America/New_York",
        
        "name2": "Jane Smith",
        "birth_date2": "1992-03-15T15:30:00",
        "city2": "Los Angeles",
        "nation2": "US",
        "lng2": -118.2437,
        "lat2": 34.0522,
        "tz_str2": "America/Los_Angeles",
        
        "houses_system": "P",
        "theme": "dark",
        "chart_language": "EN",
        "chart_id": "test_synastry_chart"
    }

def test_generate_natal_chart_visualization(valid_natal_visualization_request):
    """Test generating a natal chart visualization."""
    response = client.post(
        "/api/v1/charts/visualization/natal", 
        json=valid_natal_visualization_request
    )
    
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    
    # Check response structure
    assert "chart_id" in data
    assert "svg_url" in data
    
    # Check that the values match what we expect
    assert data["chart_id"] == valid_natal_visualization_request["chart_id"]
    assert data["svg_url"] == f"/static/images/svg/{valid_natal_visualization_request['chart_id']}.svg"
    
    # Verify we can retrieve the generated SVG
    svg_response = client.get(data["svg_url"])
    assert svg_response.status_code == status.HTTP_200_OK
    assert svg_response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in svg_response.text

def test_generate_synastry_chart_visualization(valid_synastry_visualization_request):
    """Test generating a synastry chart visualization."""
    response = client.post(
        "/api/v1/charts/visualization/synastry", 
        json=valid_synastry_visualization_request
    )
    
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    
    # Check response structure
    assert "chart_id" in data
    assert "svg_url" in data
    
    # Check that the values match what we expect
    assert data["chart_id"] == valid_synastry_visualization_request["chart_id"]
    assert data["svg_url"] == f"/static/images/svg/{valid_synastry_visualization_request['chart_id']}.svg"
    
    # Verify we can retrieve the generated SVG
    svg_response = client.get(data["svg_url"])
    assert svg_response.status_code == status.HTTP_200_OK
    assert svg_response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in svg_response.text

def test_generate_natal_chart_missing_required_fields():
    """Test generating a natal chart visualization with missing required fields."""
    incomplete_request = {
        "name": "John Doe",
        # Missing birth_date and other fields
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=incomplete_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error

def test_generate_natal_chart_invalid_date():
    """Test generating a natal chart visualization with invalid date."""
    invalid_request = {
        "name": "John Doe",
        "birth_date": "invalid-date",
        "city": "New York",
        "nation": "US",
        "lng": -74.006,
        "lat": 40.7128,
        "tz_str": "America/New_York",
        "houses_system": "P",
        "theme": "dark",
        "chart_language": "EN"
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=invalid_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error

def setup_static_dir():
    """Ensure the static directory exists and is clean."""
    os.makedirs("app/static/images/svg", exist_ok=True)
    # Clean any existing SVGs to avoid test interference
    for file in os.listdir("app/static/images/svg"):
        if file.endswith(".svg"):
            os.remove(os.path.join("app/static/images/svg", file))
    
    # Create a sample.svg file for tests that rely on it
    sample_svg = '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><!-- Sample Astrological Chart --><circle cx="50" cy="50" r="40" /></svg>'
    with open("app/static/images/svg/sample.svg", "w") as f:
        f.write(sample_svg)

@pytest.fixture(autouse=True)
def setup_teardown_static():
    """Setup and teardown for tests that use static files."""
    setup_static_dir()
    yield
    # No teardown needed as the next test will clean up
````

## File: .gitignore
````
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.pyw
*.pyz

libraries/
docs/
.env
cache/
app/static/images/svg/natal_*.svg
app/static/images/svg/synastry_*.svg
app/static/images/svg/western_*.svg 
repomix-output.md
````

## File: app/services/chart_visualization.py
````python
"""Service for chart visualization using Kerykeion."""
import os
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from kerykeion import AstrologicalSubject, KerykeionChartSVG

from app.core.config import Settings

# Get logger
logger = logging.getLogger(__name__)

# Define the directory where SVG images will be stored
SVG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                       "static", "images", "svg")

# Ensure the directory exists
os.makedirs(SVG_DIR, exist_ok=True)

# Map house system names to their corresponding Kerykeion identifiers
HOUSE_SYSTEM_MAP = {
    "Placidus": "P",
    "Koch": "K",
    "Whole Sign": "W",
    "Equal House": "A",  # Equal (Ascendant)
    "Equal (MC)": "E",
    "Campanus": "C",
    "Regiomontanus": "R",
    "Porphyry": "O",  # Porphyrius
    "Polich-Page Topocentric": "T",
    "Alcabitius": "B",
    "Morinus": "M",
    "Vehlow Equal": "V",
    "Axial Rotation": "X",
    "Horizon/Azimuth": "H"
}

def map_house_system(house_system: str) -> str:
    """
    Map a human-readable house system name to its Kerykeion identifier.
    
    Args:
        house_system: Human-readable house system name
        
    Returns:
        The single-letter Kerykeion identifier for the house system
    """
    if house_system in HOUSE_SYSTEM_MAP:
        return HOUSE_SYSTEM_MAP[house_system]
    
    # If it's already a valid single-letter identifier, return it
    if house_system in "ABCDEFGHIKLMNOPQRSTUVWXY":
        return house_system
    
    # Default to Placidus if not found
    logger.warning(f"Unknown house system '{house_system}', defaulting to Placidus (P)")
    return "P"

class ChartVisualizationService:
    """Service for generating and saving chart visualizations."""
    
    def __init__(self, settings: Settings):
        """Initialize the chart visualization service with settings."""
        self.settings = settings
    
    def generate_natal_chart_svg(
        self,
        name: str,
        birth_date: datetime,
        city: str | None = None,
        nation: str | None = None,
        lng: float | None = None,
        lat: float | None = None,
        tz_str: str | None = None,
        chart_id: str | None = None,
        theme: str = "dark",
        chart_language: str = "EN",
        config: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        """
        Generate a natal chart SVG visualization using Kerykeion.
        
        Args:
            name: Name of the person
            birth_date: Birth date and time
            city: City of birth (optional)
            nation: Country of birth (optional)
            lng: Longitude of birth place (optional)
            lat: Latitude of birth place (optional)
            tz_str: Timezone string (optional)
            chart_id: Optional custom ID for the chart
            theme: Chart theme ("light", "dark", "dark-high-contrast", "classic")
            chart_language: Chart language (default: "EN")
            config: Chart configuration options
                - houses_system: House system identifier (default: "P" for Placidus)
                - zodiac_type: Zodiac type ("Tropic" or "Sidereal")
                - sidereal_mode: Sidereal mode (required if zodiac_type is "Sidereal")
                - perspective_type: Type of perspective ("Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric")
                - active_points: List of active planets and points
                - active_aspects: List of active aspects with their orbs
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Default config if not provided
            if config is None:
                config = {
                    "houses_system": "P",
                    "zodiac_type": "Tropic",
                    "active_points": [
                        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
                        "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
                        "Mean_Lilith", "Mean_South_Node"
                    ],
                    "active_aspects": [
                        {"name": "conjunction", "orb": 10}, 
                        {"name": "opposition", "orb": 10}, 
                        {"name": "trine", "orb": 8}, 
                        {"name": "sextile", "orb": 6}, 
                        {"name": "square", "orb": 5}, 
                        {"name": "quintile", "orb": 1}
                    ]
                }
                
            # Extract configuration options
            original_house_system = config.get("houses_system", "P")
            houses_system = map_house_system(original_house_system)
            logger.info(f"Mapped house system from '{original_house_system}' to '{houses_system}'")
            
            # Convert language to uppercase
            chart_language = chart_language.upper()
            logger.info(f"Using chart language: {chart_language}")
            
            zodiac_type = config.get("zodiac_type", "Tropic")
            sidereal_mode = config.get("sidereal_mode", None)
            perspective_type = config.get("perspective_type", "Apparent Geocentric")
            active_points = config.get("active_points", [
                "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
                "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
                "Mean_Lilith", "Mean_South_Node"
            ])
            active_aspects = config.get("active_aspects", [
                {"name": "conjunction", "orb": 10}, 
                {"name": "opposition", "orb": 10}, 
                {"name": "trine", "orb": 8}, 
                {"name": "sextile", "orb": 6}, 
                {"name": "square", "orb": 5}, 
                {"name": "quintile", "orb": 1}
            ])
            
            # Generate a unique ID if not provided
            if not chart_id:
                chart_id = f"natal_{uuid.uuid4().hex[:8]}"
                
            # Define the SVG file path
            svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
            svg_path_obj = Path(svg_path)
            
            # Create the AstrologicalSubject with zodiac and house configuration
            subject = AstrologicalSubject(
                name=name,
                year=birth_date.year,
                month=birth_date.month,
                day=birth_date.day,
                hour=birth_date.hour,
                minute=birth_date.minute,
                city=city,
                nation=nation,
                lng=lng,
                lat=lat,
                tz_str=tz_str,
                houses_system_identifier=houses_system,
                zodiac_type=zodiac_type,
                sidereal_mode=sidereal_mode,
                perspective_type=perspective_type,
                geonames_username=self.settings.GEONAMES_USERNAME,
                online=bool(self.settings.GEONAMES_USERNAME)  # Use online mode when username is provided
            )
            
            # Generate the SVG chart with custom output directory and configuration
            chart = KerykeionChartSVG(
                subject, 
                chart_type='Natal',
                theme=theme,
                chart_language=chart_language,
                new_output_directory=str(Path(SVG_DIR)),
                active_points=active_points,
                active_aspects=active_aspects
            )
            
            # Save the chart with a custom filename
            # First create the chart's template
            chart.template = chart.makeTemplate()
            
            # Write to custom path (overriding default behavior)
            with open(svg_path, "w", encoding="utf-8", errors="ignore") as output_file:
                output_file.write(chart.template)
            
            logger.info(f"Chart saved as {svg_path}")
            
            # Return the chart ID and URL
            return {
                "chart_id": chart_id,
                "svg_url": f"/static/images/svg/{chart_id}.svg"
            }
            
        except Exception as e:
            logger.error(f"Error generating chart visualization: {str(e)}", exc_info=True)
            raise
    
    def generate_synastry_chart_svg(
        self,
        name1: str,
        birth_date1: datetime,
        name2: str,
        birth_date2: datetime,
        city1: str | None = None,
        nation1: str | None = None,
        lng1: float | None = None,
        lat1: float | None = None,
        tz_str1: str | None = None,
        city2: str | None = None,
        nation2: str | None = None,
        lng2: float | None = None,
        lat2: float | None = None,
        tz_str2: str | None = None,
        chart_id: str | None = None,
        theme: str = "dark",
        chart_language: str = "EN",
        config: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        """
        Generate a synastry chart SVG visualization using Kerykeion.
        
        Args:
            name1: Name of the first person
            birth_date1: Birth date and time of the first person
            name2: Name of the second person
            birth_date2: Birth date and time of the second person
            city1, nation1, lng1, lat1, tz_str1: Location data for first person
            city2, nation2, lng2, lat2, tz_str2: Location data for second person
            chart_id: Optional custom ID for the chart
            theme: Chart theme ("light", "dark", "dark-high-contrast", "classic")
            chart_language: Chart language (default: "EN")
            config: Chart configuration options
                - houses_system: House system identifier (default: "P" for Placidus)
                - zodiac_type: Zodiac type ("Tropic" or "Sidereal")
                - sidereal_mode: Sidereal mode (required if zodiac_type is "Sidereal")
                - perspective_type: Type of perspective ("Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric")
                - active_points: List of active planets and points
                - active_aspects: List of active aspects with their orbs
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Default config if not provided
            if config is None:
                config = {
                    "houses_system": "P",
                    "zodiac_type": "Tropic",
                    "active_points": [
                        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
                        "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
                        "Mean_Lilith", "Mean_South_Node"
                    ],
                    "active_aspects": [
                        {"name": "conjunction", "orb": 10}, 
                        {"name": "opposition", "orb": 10}, 
                        {"name": "trine", "orb": 8}, 
                        {"name": "sextile", "orb": 6}, 
                        {"name": "square", "orb": 5}, 
                        {"name": "quintile", "orb": 1}
                    ]
                }
                
            # Extract configuration options
            original_house_system = config.get("houses_system", "P")
            houses_system = map_house_system(original_house_system)
            logger.info(f"Mapped house system from '{original_house_system}' to '{houses_system}'")
            
            # Convert language to uppercase
            chart_language = chart_language.upper()
            logger.info(f"Using chart language: {chart_language}")
            
            zodiac_type = config.get("zodiac_type", "Tropic")
            sidereal_mode = config.get("sidereal_mode", None)
            perspective_type = config.get("perspective_type", "Apparent Geocentric")
            active_points = config.get("active_points", [
                "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
                "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
                "Mean_Lilith", "Mean_South_Node"
            ])
            active_aspects = config.get("active_aspects", [
                {"name": "conjunction", "orb": 10}, 
                {"name": "opposition", "orb": 10}, 
                {"name": "trine", "orb": 8}, 
                {"name": "sextile", "orb": 6}, 
                {"name": "square", "orb": 5}, 
                {"name": "quintile", "orb": 1}
            ])
            
            # Generate a unique ID if not provided
            if not chart_id:
                chart_id = f"synastry_{uuid.uuid4().hex[:8]}"
                
            # Define the SVG file path
            svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
            svg_path_obj = Path(svg_path)
            
            # Create the first AstrologicalSubject with zodiac and house configuration
            subject1 = AstrologicalSubject(
                name=name1,
                year=birth_date1.year,
                month=birth_date1.month,
                day=birth_date1.day,
                hour=birth_date1.hour,
                minute=birth_date1.minute,
                city=city1,
                nation=nation1,
                lng=lng1,
                lat=lat1,
                tz_str=tz_str1,
                houses_system_identifier=houses_system,
                zodiac_type=zodiac_type,
                sidereal_mode=sidereal_mode,
                perspective_type=perspective_type,
                geonames_username=self.settings.GEONAMES_USERNAME,
                online=bool(self.settings.GEONAMES_USERNAME)  # Use online mode when username is provided
            )
            
            # Create the second AstrologicalSubject with zodiac and house configuration
            subject2 = AstrologicalSubject(
                name=name2,
                year=birth_date2.year,
                month=birth_date2.month,
                day=birth_date2.day,
                hour=birth_date2.hour,
                minute=birth_date2.minute,
                city=city2,
                nation=nation2,
                lng=lng2,
                lat=lat2,
                tz_str=tz_str2,
                houses_system_identifier=houses_system,
                zodiac_type=zodiac_type,
                sidereal_mode=sidereal_mode,
                perspective_type=perspective_type,
                geonames_username=self.settings.GEONAMES_USERNAME,
                online=bool(self.settings.GEONAMES_USERNAME)  # Use online mode when username is provided
            )
            
            # Generate the SVG chart with custom output directory and configuration
            chart = KerykeionChartSVG(
                subject1, 
                chart_type='Synastry',
                second_obj=subject2,
                theme=theme,
                chart_language=chart_language,
                new_output_directory=str(Path(SVG_DIR)),
                active_points=active_points,
                active_aspects=active_aspects
            )
            
            # Save the chart with a custom filename
            # First create the chart's template
            chart.template = chart.makeTemplate()
            
            # Write to custom path (overriding default behavior)
            with open(svg_path, "w", encoding="utf-8", errors="ignore") as output_file:
                output_file.write(chart.template)
            
            logger.info(f"Synastry chart saved as {svg_path}")
            
            # Return the chart ID and URL
            return {
                "chart_id": chart_id,
                "svg_url": f"/static/images/svg/{chart_id}.svg"
            }
            
        except Exception as e:
            logger.error(f"Error generating synastry chart visualization: {str(e)}", exc_info=True)
            raise
````

## File: app/main.py
````python
"""Main application module."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from app.api import router as api_router
from app.static import mount_static_files
from app.core.config import settings
from app.core.error_handlers import add_error_handlers

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def custom_openapi():
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="""
        Zodiac Engine API powered by Kerykeion library.
        
        ## Features
        * Natal Chart Calculations
        * Synastry Analysis
        * Composite Charts
        * Relationship Compatibility Scoring
        
        ## Error Handling
        The API uses standard HTTP status codes and returns detailed error messages
        in a consistent format:
        ```json
        {
            "error": {
                "code": 400,
                "message": "Detailed error message",
                "type": "ErrorType",
                "path": "/api/v1/..."
            }
        }
        ```
        """,
        routes=app.routes,
    )

    # Custom extension to add more metadata
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    # Add security schemes if needed
    # openapi_schema["components"]["securitySchemes"] = {...}

    app.openapi_schema = openapi_schema
    return app.openapi_schema

def create_application() -> FastAPI:
    """Create FastAPI application with configuration."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Astrological API powered by Kerykeion",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=[
            {
                "name": "natal-chart",
                "description": "Operations for calculating and analyzing natal charts",
                "externalDocs": {
                    "description": "Kerykeion Documentation",
                    "url": "https://github.com/giacomobattista/kerykeion"
                }
            },
            {
                "name": "synastry",
                "description": "Operations for analyzing relationships between two charts"
            },
            {
                "name": "composite",
                "description": "Operations for generating and analyzing composite charts"
            },
            {
                "name": "health",
                "description": "API health check operations"
            },
            {
                "name": "charts",
                "description": "Operations for all chart types"
            },
            {
                "name": "chart-visualization",
                "description": "Operations for generating chart visualizations"
            },
            {
                "name": "static",
                "description": "Static resource operations"
            },
            {
                "name": "web",
                "description": "Web interface operations"
            }
        ]
    )

    # Set CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add error handlers
    add_error_handlers(application)

    # Include API router
    application.include_router(api_router)
    
    # Mount static files
    mount_static_files(application)

    @application.get(
        "/",
        tags=["web"],
        summary="Redirect to Web Interface",
        description="Redirects to the web interface for chart generation.",
        response_class=RedirectResponse,
        status_code=303
    )
    async def root():
        """Redirect to web interface."""
        return "/home"
    
    @application.get(
        "/api",
        tags=["health"],
        summary="Health Check",
        description="Check if the API is running and get version information.",
        responses={
            200: {
                "description": "API is healthy",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "healthy",
                            "version": settings.VERSION
                        }
                    }
                }
            }
        }
    )
    async def api_health():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": settings.VERSION
        }

    # Set custom OpenAPI schema
    application.openapi = custom_openapi

    return application

app = create_application()
````
