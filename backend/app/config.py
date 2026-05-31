"""Configuration settings"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # API
    API_TITLE = "Werewolf Game API"
    API_VERSION = "0.1.0"
    
    # Database
    # Default to SQLite for local development
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./werewolf.db"
    )
    
    # WebSocket
    WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
    WS_PORT = int(os.getenv("WS_PORT", 8000))
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"
    
    # Secrets
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")


settings = Settings()
