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

class FileConversionError(ZodiacEngineException):
    """Exception for errors during file format conversion."""
    def __init__(self, detail: str = "Error converting file format"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        ) 