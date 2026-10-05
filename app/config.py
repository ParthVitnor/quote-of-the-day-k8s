"""
Configuration management for Quote of the Day application.
Loads environment variables and provides configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://quoteuser:changeme@localhost:5432/quotedb"
    )
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "quotedb")
    DB_USER: str = os.getenv("DB_USER", "quoteuser")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "changeme")
    
    # Application configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")
    DATA_DIR: str = os.path.join(BASE_DIR, "data")


# Global settings instance
settings = Settings()
