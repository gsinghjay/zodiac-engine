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