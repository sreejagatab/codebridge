"""
Core configuration management
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = "CodeBridge"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 3047
    
    # CORS Configuration
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./codebridge.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./codebridge.db"
    DATABASE_ECHO: bool = False  # Set to True to log SQL queries
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    # Security
    SECRET_KEY: str = "codebridge-jwt-secret-key-change-in-production-please"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    STRICT_RATE_LIMIT_PER_MINUTE: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
