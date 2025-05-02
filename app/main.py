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