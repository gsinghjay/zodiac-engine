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