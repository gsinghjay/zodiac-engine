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