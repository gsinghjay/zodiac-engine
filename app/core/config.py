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