import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file if it exists
load_dotenv()

def get_required_env(key: str) -> str:
    """Get a required environment variable or raise an error"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value

class Settings:
    # MongoDB Configuration
    MONGODB_URI: str = get_required_env("MONGODB_URI")
    
    # Encryption Configuration
    ENCRYPTION_KEY: str = get_required_env("ENCRYPTION_KEY")
    
    # Environment (development, production, etc.)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    # Security
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "*").split(",")
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

# Global settings instance
settings = Settings()
