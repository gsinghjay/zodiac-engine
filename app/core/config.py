from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    ALLOWED_ORIGINS: str
    
    # Kerykeion settings
    GEONAMES_USERNAME: str
    
    # LLM API settings
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL_NAME: Optional[str] = None
    LLM_PROVIDER: Optional[str] = "openai"  # Options: "openai", "anthropic", "gemini"
    LLM_MAX_TOKENS: Optional[int] = 2000
    LLM_TEMPERATURE: Optional[float] = 0.7
    LLM_CACHE_ENABLED: Optional[bool] = True
    LLM_CACHE_TTL_HOURS: Optional[int] = 24  # Cache TTL in hours

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
        
    @property
    def llm_config(self) -> dict:
        """Get LLM configuration as a dictionary."""
        return {
            "api_key": self.LLM_API_KEY,
            "model_name": self.LLM_MODEL_NAME,
            "provider": self.LLM_PROVIDER,
            "max_tokens": self.LLM_MAX_TOKENS,
            "temperature": self.LLM_TEMPERATURE,
            "cache_enabled": self.LLM_CACHE_ENABLED,
            "cache_ttl_hours": self.LLM_CACHE_TTL_HOURS
        }

settings = Settings() 