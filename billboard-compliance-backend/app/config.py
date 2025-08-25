"""Configuration settings for the Billboard Compliance application.

This module defines the application's configuration settings using Pydantic,
which allows for environment variable overrides and type validation.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings with default values and environment variable overrides.
    
    Attributes:
        database_hostname: Database server hostname
        database_port: Database server port
        database_password: Database password
        database_name: Name of the database
        database_username: Database username
        secret_key: Secret key for JWT token generation
        algorithm: Algorithm used for JWT tokens
        access_token_expire_minutes: Token expiration time in minutes
    """
    database_hostname: str = "localhost"
    database_port: str = "3306"  # Default MySQL/MariaDB port
    database_password: str = ""  # Your MySQL password
    database_name: str = "billboard_compliance"
    database_username: str = "root"  # Default MySQL username
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        """Pydantic config class for settings."""
        env_file = ".env"

settings = Settings()
