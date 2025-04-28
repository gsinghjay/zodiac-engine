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
      endpoints/
        charts/
          __init__.py
          composite.py
          natal.py
          synastry.py
          transit.py
          visualization.py
        __init__.py
      __init__.py
    __init__.py
  core/
    config.py
    dependencies.py
    error_handlers.py
    exceptions.py
  routers/
    __init__.py
  schemas/
    chart_visualization.py
    natal_chart.py
  services/
    astrology.py
    chart_visualization.py
  static/
    __init__.py
  main.py
tests/
  conftest.py
  test_chart_configuration.py
  test_charts_natal.py
  test_natal_chart_variations.py
  test_static_images.py
.gitignore
.repomixignore
CHANGELOG.md
fastapi-best-practices-updates.md
pytest.ini
README.md
requirements.txt
```

# Files

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

The schemas use Pydantic features like:
- Type annotations for validation
- Field descriptors with examples
- Default values
- Documentation for OpenAPI schema

## Modernization Recommendations

We recommend updating the schemas to use latest Pydantic v2 features:
- Use new type syntax (`str | None` instead of `Optional[str]`)
- Update model configuration style
- Implement stronger validation rules

Full recommendations are available in the [fastapi-best-practices-updates.md](mdc:fastapi-best-practices-updates.md) file.
````

## File: .cursor/rules/fastapi-best-practices.mdc
````
---
description: 
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

## Detailed Implementation Plan
The full implementation plan is documented in [fastapi-best-practices-updates.md](mdc:fastapi-best-practices-updates.md)
````

## File: .cursor/rules/fastapi-testing.mdc
````
---
description: his rule documents best practices for writing FastAPI tests in the Zodiac Engine. Call this rule when reviewing or creating tests, implementing test fixtures, or working with async testing. Use it when users need guidance on test structure, mocking dependencies, handling async operations, or optimizing test performance.
globs: 
alwaysApply: false
---
# FastAPI Testing Best Practices

This document outlines the recommended testing practices for the Zodiac Engine application.

## Test Structure

- **Test Organization**: Organize tests by API resources/endpoints rather than by feature to improve maintainability
- **Test Files**: Name test files with `test_` prefix (e.g., `test_natal_charts.py`)
- **Test Directory**: Keep all tests in the `tests/` directory at the project root

## TestClient Usage

The primary way to test FastAPI endpoints is with `TestClient`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_endpoint():
    response = client.get("/some-endpoint")
    assert response.status_code == 200
    assert response.json() == {"expected": "response"}
```

## Asynchronous Testing

For testing async endpoints correctly, use the following pattern:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.anyio  # Use anyio instead of asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/endpoint")
    assert response.status_code == 200
```

## Using Fixtures

Place common fixtures in `conftest.py` for better reuse:

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_data():
    return {
        "name": "Test Person",
        "birth_date": "1990-01-01T12:00:00",
        # other test data
    }
```

## Dependency Overrides

Override dependencies for isolated testing:

```python
from app.main import app, get_service

# Create test service
def get_test_service():
    return TestService()

# Override for testing
app.dependency_overrides[get_service] = get_test_service

# Reset after testing
def teardown():
    app.dependency_overrides = {}
```

## Best Practices

1. **Test Both Success and Error Cases**: Verify correct behavior for both valid and invalid inputs
2. **Parameterized Testing**: Use `@pytest.mark.parametrize` for testing variations
3. **Mocking External Services**: Use `unittest.mock` or pytest's monkeypatch to avoid actual API calls
4. **Testing File Operations**: Consider mocking file operations instead of writing actual files
5. **Test Coverage**: Use pytest-cov to analyze and maintain test coverage

## Project-Specific Guidelines

- Test all chart generation endpoints with different parameter combinations
- Verify SVG generation using content checks rather than file existence when possible
- Mock the Kerykeion library calls for faster tests that don't depend on the library's behavior
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
  - Main endpoints: [app/api/v1/endpoints/charts](mdc:app/api/v1/endpoints/charts)
  - Natal charts: [app/api/v1/endpoints/charts/natal.py](mdc:app/api/v1/endpoints/charts/natal.py)
  - Visualizations: [app/api/v1/endpoints/charts/visualization.py](mdc:app/api/v1/endpoints/charts/visualization.py)

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
- Each endpoint group has its own module in [app/api/v1/endpoints](mdc:app/api/v1/endpoints)

## Key API Endpoints

### Chart Endpoints

The primary endpoints for astrological charts are located in [app/api/v1/endpoints/charts](mdc:app/api/v1/endpoints/charts):

- **Natal Charts**: [app/api/v1/endpoints/charts/natal.py](mdc:app/api/v1/endpoints/charts/natal.py)
  - Calculates complete natal charts based on birth data
  - Endpoint: `POST /api/v1/charts/natal/`

- **Chart Visualization**: [app/api/v1/endpoints/charts/visualization.py](mdc:app/api/v1/endpoints/charts/visualization.py)
  - Generates SVG visualizations of charts
  - Endpoints: 
    - `POST /api/v1/charts/visualization/natal`
    - `POST /api/v1/charts/visualization/synastry`

- **Synastry**: [app/api/v1/endpoints/charts/synastry.py](mdc:app/api/v1/endpoints/charts/synastry.py)
  - Analyzes relationships between two charts
  - Endpoint: `POST /api/v1/charts/synastry/`

- **Composite**: [app/api/v1/endpoints/charts/composite.py](mdc:app/api/v1/endpoints/charts/composite.py)
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

The current service implementation uses static methods, but we recommend:
- Converting to instance methods
- Implementing dependency injection
- Adding appropriate caching for performance
- Making async methods where I/O operations are performed

See [fastapi-best-practices-updates.md](mdc:fastapi-best-practices-updates.md) for improvement recommendations for the service layer.
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
````

## File: fastapi-best-practices-updates.md
````markdown
# FastAPI Best Practices Updates for Zodiac Engine

This document outlines the necessary updates to align the Zodiac Engine application with the latest FastAPI best practices.

## 1. Dependencies and Requirements

### 1.1 Update requirements.txt
- Replace `fastapi[all]` with specific dependencies:
  ```
  fastapi>=0.112.0,<0.113.0
  uvicorn[standard]>=0.34.0,<0.35.0
  pydantic>=2.11.0,<2.12.0
  pydantic-settings>=2.8.0,<2.9.0
  ```
- Add explicit version constraints for all dependencies
- Specify minimum and maximum versions for critical packages

### 1.2 Environment Variables
- Update Settings class to use .env file integration:
  ```python
  class Settings(BaseSettings):
      PROJECT_NAME: str
      VERSION: str
      API_V1_STR: str
      ALLOWED_ORIGINS: list[str] = ["*"]
      GEONAMES_USERNAME: str
      
      class Config:
          env_file = ".env"
          env_file_encoding = "utf-8"
  ```
- Document required environment variables in README.md

## 2. Pydantic Model Modernization

### 2.1 Update Type Hints
- Replace `Optional[str]` with `str | None`
- Replace `Union[str, None]` with `str | None`
- Replace `List[Type]` with `list[Type]`
- Replace `Dict[KeyType, ValueType]` with `dict[KeyType, ValueType]`

### 2.2 Update Model Configuration
- Replace `class Config` with `model_config`:
  ```python
  # Old style
  class Config:
      json_schema_extra = {...}
      
  # New style
  model_config = {
      "json_schema_extra": {...}
  }
  ```

### 2.3 Field Validations
- Use the new field validators from Pydantic v2
- Add proper constraint messages for better error reporting

## 3. Dependency Injection Patterns

### 3.1 Use Annotated Type Hints
- Update all dependencies to use `Annotated[Type, Depends()]`:
  ```python
  # Old style
  async def endpoint(settings: Settings = Depends(get_settings)):
      ...
      
  # New style
  async def endpoint(settings: Annotated[Settings, Depends(get_settings)]):
      ...
  ```
- Create type aliases for commonly used dependencies

### 3.2 Service Dependencies
- Convert static service methods to instance methods
- Create factory functions for services:
  ```python
  def get_astrology_service():
      return AstrologyService()
      
  @router.post("/")
  async def calculate_natal_chart(
      request: NatalChartRequest,
      astrology_service: Annotated[AstrologyService, Depends(get_astrology_service)]
  ):
      return astrology_service.calculate_natal_chart(...)
  ```

### 3.3 Dependency Caching
- Apply `@lru_cache` appropriately to expensive dependencies
- Consider when to use `use_cache=False` for dependencies that need fresh data

## 4. Async/Sync Consistency

### 4.1 Endpoint Functions
- Use `async def` only for endpoints that perform async I/O operations
- Convert non-async operations to sync functions:
  ```python
  # If no async operations are performed
  @router.post("/")
  def calculate_natal_chart(request: NatalChartRequest):
      return AstrologyService.calculate_natal_chart(...)
  ```

### 4.2 Service Methods
- Make service methods async if they perform I/O operations
- Keep pure computation methods as sync

### 4.3 Consistent Calling Patterns
- Use `await` properly for async functions
- Avoid mixing sync and async patterns

## 5. Error Handling Improvements

### 5.1 Use FastAPI Status Codes
- Import from `fastapi import status`
- Use constants like `status.HTTP_201_CREATED`:
  ```python
  @router.post(
      "/",
      response_model=NatalChartResponse,
      status_code=status.HTTP_201_CREATED
  )
  ```

### 5.2 Exception Handling
- Improve redundant try/except blocks
- Use the global exception handler consistently
- Add more specific exception types if needed

### 5.3 Response Consistency
- Standardize error response formats
- Add more descriptive error messages

## 6. API Response Customization

### 6.1 Response Model Options
- Use `response_model_exclude_unset=True` where appropriate:
  ```python
  @router.post(
      "/natal",
      response_model=NatalChartResponse,
      response_model_exclude_unset=True
  )
  ```
- Consider `response_model_exclude_defaults=True` for reduced payload
- Add proper response descriptions

### 6.2 Response Status Codes
- Use appropriate status codes for different operations
- Document the status codes in OpenAPI

## 7. Performance Optimizations

### 7.1 Background Tasks
- Use FastAPI's background tasks for long-running operations:
  ```python
  @router.post("/natal")
  async def generate_natal_chart_visualization(
      request: NatalChartVisualizationRequest,
      background_tasks: BackgroundTasks,
      settings: Annotated[Settings, Depends(get_settings)]
  ):
      chart_id = f"natal_{uuid.uuid4().hex[:8]}"
      result = {"chart_id": chart_id, "status": "processing"}
      background_tasks.add_task(
          ChartVisualizationService.generate_natal_chart_svg,
          name=request.name,
          # other parameters...
      )
      return result
  ```
- Implement a task queue for heavy processing

### 7.2 Caching Strategies
- Add caching for expensive calculations
- Consider Redis or similar for distributed caching

## Implementation Plan

1. Update dependencies and requirements first
2. Modernize Pydantic models
3. Improve dependency injection patterns
4. Fix async/sync inconsistencies
5. Enhance error handling
6. Optimize API responses
7. Implement performance optimizations
````

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

## File: app/api/v1/endpoints/charts/composite.py
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

## File: app/api/v1/endpoints/charts/synastry.py
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

## File: app/api/v1/endpoints/charts/transit.py
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

## File: app/api/v1/endpoints/__init__.py
````python
"""API v1 endpoints initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints.charts import router as charts_router

# Create the endpoints router
router = APIRouter()

# Include charts router
router.include_router(charts_router)

# Export the router for use in the main v1 router
__all__ = ["router"]
````

## File: app/api/v1/__init__.py
````python
"""API v1 router initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints import router as endpoints_router

# Create the main v1 router with prefix and tag
router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

# Include endpoints router
router.include_router(endpoints_router)

# Export the router for use in the main API router
__all__ = ["router"]
````

## File: app/api/__init__.py
````python
"""API router initialization."""
from fastapi import APIRouter

from app.api.v1 import router as v1_router

# Create the main API router
router = APIRouter()

# Include API version routers
router.include_router(v1_router)

# Export the router for use in the main app
__all__ = ["router"]
````

## File: app/core/dependencies.py
````python
"""Dependency functions for FastAPI."""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings

@lru_cache
def get_settings() -> Settings:
    """
    Get application settings as a dependency.
    
    Uses lru_cache for caching to avoid reloading settings on every request.
    """
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
````

## File: app/core/error_handlers.py
````python
"""Global exception handlers for the application."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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
                    "path": request.url.path
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
        if "InvalidDateError" in str(type(exc)):
            status_code = 400
            message = str(exc)
            error_type = "InvalidDateError"
        elif "InvalidCoordinatesError" in str(type(exc)):
            status_code = 400
            message = str(exc)
            error_type = "InvalidCoordinatesError"
        else:
            status_code = 500
            message = "Internal server error"
            error_type = type(exc).__name__

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

## File: app/routers/__init__.py
````python
"""Routers initialization."""
from fastapi import APIRouter

from app.routers.static import router as static_router

# Create the main router
router = APIRouter()

# Include static router
router.include_router(static_router)

# Export the router for use in the main app
__all__ = ["router"]
````

## File: app/static/__init__.py
````python
"""Static files initialization."""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Define path to static files
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

def mount_static_files(app: FastAPI) -> None:
    """Mount static files to the FastAPI application."""
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
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

## File: tests/test_chart_configuration.py
````python
"""Tests for chart configuration features."""
import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

client = TestClient(app)

# Test data
TEST_NATAL_DATA = {
    "name": "Test Person",
    "birth_date": "1990-01-01T12:00:00",
    "lng": -74.006,  # New York coordinates
    "lat": 40.7128,
    "tz_str": "America/New_York",
    "language": "EN",
    "theme": "dark"
}

@pytest.mark.asyncio
async def test_natal_chart_with_tropical_zodiac():
    """Test generating a natal chart with tropical zodiac."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P"
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == 200
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains tropical reference 
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Tropical" in svg_content

@pytest.mark.asyncio
async def test_natal_chart_with_sidereal_zodiac():
    """Test generating a natal chart with sidereal zodiac."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Sidereal",
            "sidereal_mode": "FAGAN_BRADLEY",
            "houses_system": "P"
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == 200
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains sidereal reference (Kerykeion uses "Ayanamsa" for sidereal zodiac)
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Ayanamsa" in svg_content

@pytest.mark.asyncio
async def test_natal_chart_with_limited_planets():
    """Test generating a natal chart with limited planets."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P",
            "active_points": ["Sun", "Moon", "Ascendant", "Medium_Coeli"]
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == 200
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
    # Verify SVG file contains only the selected planets
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "Sun" in svg_content
        assert "Moon" in svg_content
        # Checking that other planets like Saturn are not included
        # would be brittle as the SVG might contain the word Saturn in other contexts
        # so we're focusing on positive assertions

@pytest.mark.asyncio
async def test_natal_chart_with_custom_aspects():
    """Test generating a natal chart with custom aspects."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P",
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 6}
            ]
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == 200
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)

@pytest.mark.asyncio
async def test_natal_chart_with_different_house_system():
    """Test generating a natal chart with a different house system."""
    data = {
        **TEST_NATAL_DATA,
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "K"  # Koch house system
        }
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=data)
    assert response.status_code == 200
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
    
@pytest.mark.asyncio
async def test_synastry_chart_with_configuration():
    """Test generating a synastry chart with configuration."""
    data = {
        "name1": "Person One",
        "birth_date1": "1990-01-01T12:00:00",
        "lng1": -74.006,  # New York coordinates
        "lat1": 40.7128,
        "tz_str1": "America/New_York",
        
        "name2": "Person Two",
        "birth_date2": "1995-06-15T15:30:00",
        "lng2": -118.2437,  # Los Angeles coordinates
        "lat2": 34.0522,
        "tz_str2": "America/Los_Angeles",
        
        "language": "EN",
        "theme": "dark",
        "config": {
            "zodiac_type": "Tropic",
            "houses_system": "P",
            "active_points": ["Sun", "Moon", "Ascendant", "Venus", "Mars"],
            "active_aspects": [
                {"name": "conjunction", "orb": 8},
                {"name": "opposition", "orb": 8},
                {"name": "trine", "orb": 6}
            ]
        }
    }
    
    response = client.post("/api/v1/charts/visualization/synastry", json=data)
    assert response.status_code == 200
    assert "chart_id" in response.json()
    assert "svg_url" in response.json()
    
    # Verify the SVG file was created
    chart_id = response.json()["chart_id"]
    svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
    assert os.path.exists(svg_path)
````

## File: tests/test_natal_chart_variations.py
````python
"""Tests for various natal chart variations."""
import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

client = TestClient(app)

# Test data
TEST_NATAL_DATA = {
    "name": "Test Person",
    "birth_date": "1990-01-01T12:00:00",
    "lng": -74.006,  # New York coordinates
    "lat": 40.7128,
    "tz_str": "America/New_York"
}

@pytest.mark.asyncio
async def test_natal_chart_different_themes():
    """Test generating natal charts with different themes."""
    themes = ["light", "dark", "dark-high-contrast", "classic"]
    
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
        assert response.status_code == 200
        assert "chart_id" in response.json()
        assert "svg_url" in response.json()
        
        # Verify the SVG file was created
        chart_id = response.json()["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)

@pytest.mark.asyncio
async def test_natal_chart_different_languages():
    """Test generating natal charts with different languages."""
    languages = ["EN", "FR", "IT", "ES", "DE"]  # Using a subset of languages for testing
    
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
        assert response.status_code == 200
        assert "chart_id" in response.json()
        assert "svg_url" in response.json()
        
        # Verify the SVG file was created
        chart_id = response.json()["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)

@pytest.mark.asyncio
async def test_natal_chart_different_perspective_types():
    """Test generating natal charts with different perspective types."""
    perspective_types = ["Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric"]
    
    for perspective_type in perspective_types:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Tropic",
                "houses_system": "P",
                "perspective_type": perspective_type
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == 200
        assert "chart_id" in response.json()
        assert "svg_url" in response.json()
        
        # Verify the SVG file was created
        chart_id = response.json()["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
        
        # Verify the perspective type is shown in the chart
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert perspective_type in svg_content or perspective_type.replace(" ", "_").lower() in svg_content.lower()

@pytest.mark.asyncio
async def test_natal_chart_different_sidereal_modes():
    """Test generating natal charts with different sidereal modes."""
    sidereal_modes = ["FAGAN_BRADLEY", "LAHIRI", "DELUCE", "KRISHNAMURTI", "DJWHAL_KHUL"]
    
    for sidereal_mode in sidereal_modes:
        data = {
            **TEST_NATAL_DATA,
            "theme": "dark",
            "language": "EN",
            "config": {
                "zodiac_type": "Sidereal",
                "sidereal_mode": sidereal_mode,
                "houses_system": "P"
            }
        }
        
        response = client.post("/api/v1/charts/visualization/natal", json=data)
        assert response.status_code == 200
        assert "chart_id" in response.json()
        assert "svg_url" in response.json()
        
        # Verify the SVG file was created
        chart_id = response.json()["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
        
        # Verify the SVG file contains Ayanamsa reference
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert "Ayanamsa" in svg_content

@pytest.mark.asyncio
async def test_natal_chart_different_celestial_points():
    """Test generating natal charts with different celestial points."""
    point_sets = [
        ["Sun", "Moon", "Mercury", "Venus", "Mars"],  # Basic planets
        ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"],  # All planets
        ["Sun", "Moon", "Ascendant", "Medium_Coeli", "Descendant", "Imum_Coeli"],  # Main points + angles
        ["Sun", "Moon", "Chiron", "Mean_Lilith", "Mean_Node", "True_Node"],  # Special points
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
        assert response.status_code == 200
        assert "chart_id" in response.json()
        assert "svg_url" in response.json()
        
        # Verify the SVG file was created
        chart_id = response.json()["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
        
        # Verify at least one of the specified points appears in the content
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            assert any(point in svg_content for point in points)

@pytest.mark.asyncio
async def test_natal_chart_different_house_systems():
    """Test generating natal charts with different house systems."""
    # Valid house systems from the error message:
    # 'A', 'B', 'C', 'D', 'F', 'H', 'I', 'i', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'
    house_systems = ["P", "K", "C", "R", "W", "B", "M", "A", "D"]  # Placidus, Koch, Campanus, Regiomontanus, Whole Sign, Alcabitius, Morinus, Equal, Equal
    
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
        assert response.status_code == 200
        assert "chart_id" in response.json()
        assert "svg_url" in response.json()
        
        # Verify the SVG file was created
        chart_id = response.json()["chart_id"]
        svg_path = os.path.join("app", "static", "images", "svg", f"{chart_id}.svg")
        assert os.path.exists(svg_path)
````

## File: CHANGELOG.md
````markdown
# CHANGELOG


## v0.1.0 (2025-04-01)

### Chores

- Add cache directory to gitignore
  ([`3899142`](https://github.com/gsinghjay/zodiac-engine/commit/389914254dad77f37478b103ab411a7343647704))

- Add example chart SVG outputs
  ([`2efcc20`](https://github.com/gsinghjay/zodiac-engine/commit/2efcc20d90b1d9a5037e6cab6b14167e7151ad46))

- Initialize project configuration
  ([`22d84b0`](https://github.com/gsinghjay/zodiac-engine/commit/22d84b06efb26394784d7f625fb364f6dfd883f3))

### Continuous Integration

- Added semantic release
  ([`481ebc3`](https://github.com/gsinghjay/zodiac-engine/commit/481ebc3c173f9b24aa8f1f8181ec60d8b5400072))

### Documentation

- Add comprehensive README and update gitignore
  ([`3311358`](https://github.com/gsinghjay/zodiac-engine/commit/33113587d254554c40bb917567cec52edca01190))

- Update README with new chart visualization features
  ([`868d11c`](https://github.com/gsinghjay/zodiac-engine/commit/868d11c3e5389c636887b20c10f3c46d23942364))

### Features

- Add core services and data schemas
  ([`7d6476a`](https://github.com/gsinghjay/zodiac-engine/commit/7d6476a0d9033461bcd08a6ce71e0fbbefaace42))

- Add dependency injection for application settings
  ([`75547ab`](https://github.com/gsinghjay/zodiac-engine/commit/75547ab37add5f896a180759379f52e64bad19b4))

- Add house system configuration to natal chart endpoint
  ([`9e61f33`](https://github.com/gsinghjay/zodiac-engine/commit/9e61f334c81f0cf569c5d9b451eca80647ac6730))

- Add house system schema and update natal chart response
  ([`c4fce46`](https://github.com/gsinghjay/zodiac-engine/commit/c4fce46fad9e6fc3117d00e78d482a98bb251b9a))

- Add static file serving capability for chart images
  ([`ee51997`](https://github.com/gsinghjay/zodiac-engine/commit/ee519977c5de46b5f867e9f415270a8e2a8f96d8))

- Add support for additional celestial points in natal chart
  ([`557b2d2`](https://github.com/gsinghjay/zodiac-engine/commit/557b2d2ffc5bd9c01ab8ebc9444a9fa6bf5b9aa2))

- Configure main application with error handling and documentation
  ([`e6dccab`](https://github.com/gsinghjay/zodiac-engine/commit/e6dccab4ec1710a0dd389d206b0a1495f70943cb))

- Enhance chart visualization endpoints with additional options
  ([`b156346`](https://github.com/gsinghjay/zodiac-engine/commit/b1563464fa0ae758bd6921f797b92fbf9a44dfd7))

- Enhance chart visualization schemas with additional configuration options
  ([`3d24c58`](https://github.com/gsinghjay/zodiac-engine/commit/3d24c58bfc1f40fcff56c0cc269e9710c143bc98))

- Implement API structure with versioned endpoints
  ([`73cbdc1`](https://github.com/gsinghjay/zodiac-engine/commit/73cbdc170d6cc556bf6b2e4dfcea448939d53ad7))

- Implement chart visualization using Kerykeion SVG
  ([`b75a053`](https://github.com/gsinghjay/zodiac-engine/commit/b75a053ac6ba4ba77946a56c4e1ff60a2d8847c0))

- Implement extended visualization options for natal charts
  ([`f1794ae`](https://github.com/gsinghjay/zodiac-engine/commit/f1794aec806b9b2cc61015f7ebb18c889df37f87))

### Refactoring

- Move static files handling from router to FastAPI static mounting
  ([`2a36e97`](https://github.com/gsinghjay/zodiac-engine/commit/2a36e970e4d18534d6b3cf63541baeca1586808e))

### Testing

- Add comprehensive chart configuration tests
  ([`3b3a60b`](https://github.com/gsinghjay/zodiac-engine/commit/3b3a60be65cf2fc3a600595163065af858f37df3))

- Add comprehensive test suite for API endpoints
  ([`a9c4332`](https://github.com/gsinghjay/zodiac-engine/commit/a9c4332d03ceb16c710602c5a517fe4468714f8a))

- Add comprehensive tests for natal chart variations
  ([`6bfbbf2`](https://github.com/gsinghjay/zodiac-engine/commit/6bfbbf246682e7f8628fb80a9e5db4a9576e6986))

- Add tests for celestial points, aspects and house systems
  ([`3cc96d9`](https://github.com/gsinghjay/zodiac-engine/commit/3cc96d9fd8d9e4dc9e0cc6c586f86c374fa0ab02))
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

## File: requirements.txt
````
# FastAPI and its dependencies
fastapi[all]>=0.112.0,<0.113.0

# Database
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
alembic>=1.12.0

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
pytest>=7.4.3
pytest-asyncio>=0.21.1

# Utilities
python-dotenv>=1.0.0
````

## File: app/api/v1/endpoints/charts/__init__.py
````python
"""Charts router initialization."""
from fastapi import APIRouter

from app.api.v1.endpoints.charts.natal import router as natal_router
from app.api.v1.endpoints.charts.visualization import router as visualization_router

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

## File: app/api/v1/endpoints/charts/natal.py
````python
"""Natal chart router module."""
from fastapi import APIRouter, HTTPException

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
        400: {
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
        500: {
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
        200: {
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
async def calculate_natal_chart(request: NatalChartRequest) -> NatalChartResponse:
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

        return AstrologyService.calculate_natal_chart(
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

## File: app/api/v1/endpoints/charts/visualization.py
````python
"""Chart visualization API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from app.core.exceptions import ChartCalculationError, InvalidBirthDataError, LocationError
from app.core.config import Settings
from app.core.dependencies import get_settings
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
        400: {
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
        500: {
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

@router.post("/natal", response_model=NatalChartVisualizationResponse)
async def generate_natal_chart_visualization(
    request: NatalChartVisualizationRequest,
    settings: Settings = Depends(get_settings)
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
                status_code=422, 
                detail=f"Invalid birth date format: {request.birth_date}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate the chart visualization
        result = ChartVisualizationService.generate_natal_chart_svg(
            name=request.name,
            birth_date=birth_date,
            city=request.city,
            nation=request.nation,
            lng=request.lng,
            lat=request.lat,
            tz_str=request.tz_str,
            chart_id=request.chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.dict() if request.config else None,
            settings=settings
        )
        
        return NatalChartVisualizationResponse(
            chart_id=result["chart_id"],
            svg_url=result["svg_url"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart: {str(e)}")

@router.post("/synastry", response_model=SynastryChartVisualizationResponse)
async def generate_synastry_chart_visualization(
    request: SynastryChartVisualizationRequest,
    settings: Settings = Depends(get_settings)
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
                status_code=422, 
                detail=f"Invalid birth date format: {str(e)}. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
            )
        
        # Generate the synastry chart visualization
        result = ChartVisualizationService.generate_synastry_chart_svg(
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
            chart_id=request.chart_id,
            theme=request.theme,
            chart_language=request.language,
            config=request.config.dict() if request.config else None,
            settings=settings
        )
        
        return SynastryChartVisualizationResponse(
            chart_id=result["chart_id"],
            svg_url=result["svg_url"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating synastry chart: {str(e)}")
````

## File: app/core/config.py
````python
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str = "Zodiac Engine API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Kerykeion settings
    GEONAMES_USERNAME: str = ""

    class Config:
        case_sensitive = True

settings = Settings()
````

## File: app/schemas/chart_visualization.py
````python
"""Schemas for chart visualization endpoints."""
from datetime import datetime
from typing import Optional, List, Dict, Union, Literal

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
    sidereal_mode: Optional[SiderealMode] = Field(None, description="Sidereal mode (required if zodiac_type is Sidereal)")
    perspective_type: PerspectiveType = Field("Apparent Geocentric", description="Type of perspective for calculations")
    active_points: List[Union[Planet, AxialCusps]] = Field(
        default=[
            "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", 
            "Neptune", "Pluto", "Mean_Node", "Chiron", "Ascendant", "Medium_Coeli", 
            "Mean_Lilith", "Mean_South_Node"
        ],
        description="List of active planets and points to include in the chart"
    )
    active_aspects: List[AspectConfiguration] = Field(
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
    city: Optional[str] = Field(None, description="City of birth")
    nation: Optional[str] = Field(None, description="Country of birth")
    lng: Optional[float] = Field(None, description="Longitude of birth place")
    lat: Optional[float] = Field(None, description="Latitude of birth place")
    tz_str: Optional[str] = Field(None, description="Timezone string (e.g., 'America/New_York')")
    chart_id: Optional[str] = Field(None, description="Optional custom ID for the chart")
    
    # Visualization options
    theme: str = Field("dark", description="Chart theme ('light', 'dark', 'dark-high-contrast', 'classic')")
    language: str = Field("EN", description="Chart language ('EN', 'FR', 'PT', 'IT', 'CN', 'ES', 'RU', 'TR', 'DE', 'HI')")
    
    # Chart configuration
    config: Optional[ChartConfiguration] = Field(None, description="Chart configuration options")

    class Config:
        json_schema_extra = {
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

class SynastryChartVisualizationRequest(BaseModel):
    """Schema for synastry chart visualization request."""
    # First person
    name1: str = Field(..., description="Name of the first person")
    birth_date1: str = Field(..., description="Birth date and time of first person in ISO format")
    city1: Optional[str] = Field(None, description="City of birth for first person")
    nation1: Optional[str] = Field(None, description="Country of birth for first person")
    lng1: Optional[float] = Field(None, description="Longitude of birth place for first person")
    lat1: Optional[float] = Field(None, description="Latitude of birth place for first person")
    tz_str1: Optional[str] = Field(None, description="Timezone string for first person")
    
    # Second person
    name2: str = Field(..., description="Name of the second person")
    birth_date2: str = Field(..., description="Birth date and time of second person in ISO format")
    city2: Optional[str] = Field(None, description="City of birth for second person")
    nation2: Optional[str] = Field(None, description="Country of birth for second person")
    lng2: Optional[float] = Field(None, description="Longitude of birth place for second person")
    lat2: Optional[float] = Field(None, description="Latitude of birth place for second person")
    tz_str2: Optional[str] = Field(None, description="Timezone string for second person")
    
    # Shared settings
    chart_id: Optional[str] = Field(None, description="Optional custom ID for the chart")
    theme: str = Field("dark", description="Chart theme")
    language: str = Field("EN", description="Chart language")
    
    # Chart configuration
    config: Optional[ChartConfiguration] = Field(None, description="Chart configuration options")

    class Config:
        json_schema_extra = {
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

class ChartVisualizationResponse(BaseModel):
    """Schema for chart visualization response."""
    chart_id: str = Field(..., description="ID of the generated chart")
    svg_url: str = Field(..., description="URL to access the SVG visualization")

    class Config:
        json_schema_extra = {
            "example": {
                "chart_id": "natal_12345678",
                "svg_url": "/static/images/svg/natal_12345678.svg"
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
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

class PlanetPosition(BaseModel):
    """Schema for planet position in natal chart."""
    name: str = Field(..., description="Name of the planet")
    sign: str = Field(..., description="Zodiac sign the planet is in")
    position: float = Field(..., description="Position in degrees")
    house: Union[int, str] = Field(..., description="House number or name")
    retrograde: bool = Field(..., description="Whether the planet is retrograde")

class NatalChartRequest(BaseModel):
    """Schema for natal chart calculation request."""
    name: str = Field(..., description="Name of the person")
    birth_date: datetime = Field(..., description="Birth date and time")
    city: Optional[str] = Field(None, description="City of birth")
    nation: Optional[str] = Field(None, description="Country of birth")
    lng: Optional[float] = Field(None, description="Longitude of birth place")
    lat: Optional[float] = Field(None, description="Latitude of birth place")
    tz_str: Optional[str] = Field(None, description="Timezone string (e.g., 'America/New_York')")
    houses_system: Optional[str] = Field("P", description="House system identifier (e.g., 'P' for Placidus, 'W' for Whole Sign)")

    class Config:
        json_schema_extra = {
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
    planets: List[PlanetPosition] = Field(..., description="List of planet positions")
    houses: Dict[int, float] = Field(..., description="House cusps positions")
    aspects: List[AspectInfo] = Field(..., description="List of planetary aspects")
    house_system: HouseSystem = Field(..., description="House system used for calculations")
````

## File: app/services/astrology.py
````python
"""Service for astrological calculations using Kerykeion."""
import logging
from datetime import datetime
from typing import Dict, List, Union

from kerykeion import AstrologicalSubject, NatalAspects

from app.schemas.natal_chart import NatalChartResponse, PlanetPosition, AspectInfo

logger = logging.getLogger(__name__)

def _convert_house_number(house: Union[str, int]) -> Union[str, int]:
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

    @staticmethod
    def calculate_natal_chart(
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

## File: app/services/chart_visualization.py
````python
"""Service for chart visualization using Kerykeion."""
import os
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Union, List, Any

from kerykeion import AstrologicalSubject, KerykeionChartSVG

from app.core.config import Settings
from app.core.dependencies import get_settings

# Get logger
logger = logging.getLogger(__name__)

# Define the directory where SVG images will be stored
SVG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                       "static", "images", "svg")

# Ensure the directory exists
os.makedirs(SVG_DIR, exist_ok=True)

class ChartVisualizationService:
    """Service for generating and saving chart visualizations."""
    
    @staticmethod
    def generate_natal_chart_svg(
        name: str,
        birth_date: datetime,
        city: Optional[str] = None,
        nation: Optional[str] = None,
        lng: Optional[float] = None,
        lat: Optional[float] = None,
        tz_str: Optional[str] = None,
        chart_id: Optional[str] = None,
        theme: str = "dark",
        chart_language: str = "EN",
        config: Dict[str, Any] = None,
        settings: Optional[Settings] = None
    ) -> Dict[str, str]:
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
            settings: Application settings (optional)
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Get settings if not provided
            if settings is None:
                settings = get_settings()
                
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
            houses_system = config.get("houses_system", "P")
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
                geonames_username=settings.GEONAMES_USERNAME,
                online=False  # Use offline mode until we have a valid geonames username
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
    
    @staticmethod
    def generate_synastry_chart_svg(
        name1: str,
        birth_date1: datetime,
        name2: str,
        birth_date2: datetime,
        city1: Optional[str] = None,
        nation1: Optional[str] = None,
        lng1: Optional[float] = None,
        lat1: Optional[float] = None,
        tz_str1: Optional[str] = None,
        city2: Optional[str] = None,
        nation2: Optional[str] = None,
        lng2: Optional[float] = None,
        lat2: Optional[float] = None,
        tz_str2: Optional[str] = None,
        chart_id: Optional[str] = None,
        theme: str = "dark",
        chart_language: str = "EN",
        config: Dict[str, Any] = None,
        settings: Optional[Settings] = None
    ) -> Dict[str, str]:
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
            settings: Application settings (optional)
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Get settings if not provided
            if settings is None:
                settings = get_settings()
            
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
            houses_system = config.get("houses_system", "P")
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
                geonames_username=settings.GEONAMES_USERNAME,
                online=False  # Use offline mode until we have a valid geonames username
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
                geonames_username=settings.GEONAMES_USERNAME,
                online=False  # Use offline mode until we have a valid geonames username
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
            }
        ]
    )

    # Set CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
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
    async def root():
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

## File: tests/test_charts_natal.py
````python
from datetime import datetime
from typing import Dict

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture
def valid_natal_chart_request() -> Dict:
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
    
    assert response.status_code == 200
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
    assert response.status_code == 422

def test_calculate_natal_chart_missing_required():
    """Test natal chart calculation with missing required fields."""
    invalid_request = {
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/natal/", json=invalid_request)
    assert response.status_code == 422

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
    assert response.status_code == 200

def test_calculate_natal_chart_celestial_points(valid_natal_chart_request):
    """Test that all celestial points are included in the response."""
    response = client.post("/api/v1/charts/natal/", json=valid_natal_chart_request)
    
    assert response.status_code == 200
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
    
    assert response.status_code == 200
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
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the house system in the response
    assert data["house_system"]["identifier"] == "W"
    
    # House systems have different names
    assert data["house_system"]["name"] != "Placidus"
````

## File: tests/test_static_images.py
````python
"""Tests for static images routes."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_chart_svg_success():
    """Test retrieving a chart SVG image that exists."""
    response = client.get("/static/images/svg/sample.svg")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert "Sample Astrological Chart" in response.text
    assert "<svg" in response.text

def test_get_chart_svg_not_found():
    """Test retrieving a chart SVG image that doesn't exist."""
    response = client.get("/static/images/svg/nonexistent.svg")
    assert response.status_code == 404

@pytest.fixture
def valid_natal_visualization_request():
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
def valid_synastry_visualization_request():
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
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "chart_id" in data
    assert "svg_url" in data
    
    # Check that the values match what we expect
    assert data["chart_id"] == valid_natal_visualization_request["chart_id"]
    assert data["svg_url"] == f"/static/images/svg/{valid_natal_visualization_request['chart_id']}.svg"
    
    # Verify we can retrieve the generated SVG
    svg_response = client.get(data["svg_url"])
    assert svg_response.status_code == 200
    assert svg_response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in svg_response.text

def test_generate_synastry_chart_visualization(valid_synastry_visualization_request):
    """Test generating a synastry chart visualization."""
    response = client.post(
        "/api/v1/charts/visualization/synastry", 
        json=valid_synastry_visualization_request
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "chart_id" in data
    assert "svg_url" in data
    
    # Check that the values match what we expect
    assert data["chart_id"] == valid_synastry_visualization_request["chart_id"]
    assert data["svg_url"] == f"/static/images/svg/{valid_synastry_visualization_request['chart_id']}.svg"
    
    # Verify we can retrieve the generated SVG
    svg_response = client.get(data["svg_url"])
    assert svg_response.status_code == 200
    assert svg_response.headers["content-type"] == "image/svg+xml"
    assert "<svg" in svg_response.text

def test_generate_natal_chart_missing_required_fields():
    """Test generating a natal chart visualization with missing required fields."""
    incomplete_request = {
        "name": "John Doe"
        # Missing birth_date
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=incomplete_request)
    assert response.status_code == 422  # Validation error

def test_generate_natal_chart_invalid_date():
    """Test generating a natal chart visualization with invalid date."""
    invalid_request = {
        "name": "John Doe",
        "birth_date": "invalid-date",
        "city": "New York",
        "nation": "US"
    }
    
    response = client.post("/api/v1/charts/visualization/natal", json=invalid_request)
    assert response.status_code == 422  # Validation error
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
````

## File: README.md
````markdown
# Zodiac Engine

A modern astrological calculation API powered by [Kerykeion](https://github.com/giacomobattista/kerykeion) library.

## Features

- ✅ Natal Chart Calculations
- ✅ Synastry Analysis
- ✅ Composite Charts
- ✅ Transit Calculations
- ✅ SVG Chart Visualizations
- 🚧 LLM-powered Interpretations (Coming Soon)

## Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) (optional, for development)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/zodiac-engine.git
   cd zodiac-engine
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Natal Charts

```
POST /api/v1/charts/natal/
```

Calculate a complete natal chart based on birth data.

**Example Request:**

```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01T12:00:00",
  "city": "New York",
  "nation": "US",
  "lng": -74.006,
  "lat": 40.7128,
  "tz_str": "America/New_York"
}
```

### Other Chart Types

- Synastry: `POST /api/v1/charts/synastry/`
- Composite: `POST /api/v1/charts/composite/`
- Transit: `POST /api/v1/charts/transit/`

### SVG Chart Visualizations

```
POST /api/v1/charts/visualization/natal
POST /api/v1/charts/visualization/synastry
```

Generate SVG visualizations of natal and synastry charts with customizable options.

```
GET /static/images/svg/{chart_id}.svg
```

Retrieves an SVG visualization of a chart by its ID.

#### Chart Customization Options

Charts can be customized with the following configuration options:

```json
{
  "config": {
    "zodiac_type": "Tropic",           // "Tropic" or "Sidereal"
    "sidereal_mode": "FAGAN_BRADLEY",  // Required when zodiac_type is "Sidereal"
    "houses_system": "P",              // House system identifier (e.g., "P" for Placidus, "K" for Koch)
    "perspective_type": "Apparent Geocentric", // "Apparent Geocentric", "True Geocentric", "Heliocentric", "Topocentric"
    "active_points": [                 // Celestial bodies and points to include in the chart
      "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", 
      "Uranus", "Neptune", "Pluto", "Mean_Node", "Chiron", 
      "Ascendant", "Medium_Coeli"
    ],
    "active_aspects": [                // Aspects to calculate and display
      {"name": "conjunction", "orb": 10},
      {"name": "opposition", "orb": 10},
      {"name": "trine", "orb": 8},
      {"name": "sextile", "orb": 6},
      {"name": "square", "orb": 5}
    ]
  },
  "theme": "classic",                  // Chart theme: "classic", "light", "dark", "dark-high-contrast"
  "language": "EN"                     // Chart language: "EN", "FR", "PT", "IT", "CN", "ES", "RU", "TR", "DE", "HI"
}
```

**Example Request:**

```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01T12:00:00",
  "city": "New York",
  "nation": "US",
  "language": "EN",
  "theme": "dark",
  "config": {
    "zodiac_type": "Sidereal",
    "sidereal_mode": "FAGAN_BRADLEY",
    "houses_system": "K",
    "perspective_type": "Apparent Geocentric",
    "active_points": ["Sun", "Moon", "Ascendant", "Medium_Coeli"],
    "active_aspects": [
      {"name": "conjunction", "orb": 8},
      {"name": "opposition", "orb": 8}
    ]
  }
}
```

## Project Structure

```
zodiac-engine/
├── app/                    # Application package
│   ├── api/                # API endpoints
│   │   └── v1/             # Version 1 API
│   │       └── endpoints/  # API endpoint modules
│   │           └── charts/ # Chart endpoints
│   ├── core/               # Core functionality
│   ├── static/             # Static files
│   │   └── images/         # Image files
│   │       └── svg/        # SVG chart visualizations
│   ├── schemas/            # Pydantic models
│   ├── services/           # Business logic
│   └── main.py             # FastAPI application
├── tests/                  # Test package
├── .gitignore              # Git ignore file
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Development

### Setting Up Development Environment

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 guidelines and uses:
- SOLID principles
- DRY (Don't Repeat Yourself)
- Conventional commits

## Roadmap

View our development roadmap in [docs/kerykeion/task-natal-chart.md](docs/kerykeion/task-natal-chart.md).

## License

MIT License
````
