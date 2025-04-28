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