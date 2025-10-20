"""
Configuration module for the application.
Centralizes all environment variable management and provides default values.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""

    # Server Configuration
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5001'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

    # API Configuration
    API_KEY: Optional[str] = os.getenv('API_KEY')
    JWT_SECRET_KEY: Optional[str] = os.getenv('JWT_SECRET_KEY')
    JWT_EXPIRATION_HOURS: int = int(os.getenv('JWT_EXPIRATION_HOURS', '2'))

    # Application Settings
    BASE_URL: str = os.getenv('BASE_URL', f'http://127.0.0.1:{PORT}')

    # Default user credentials (for demo purposes only)
    ADMIN_USER: str = os.getenv('ADMIN_USER', 'admin')
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', 'password123')

    # Swagger/API Documentation
    API_TITLE: str = os.getenv('API_TITLE', 'Digital Library API')
    API_VERSION: str = os.getenv('API_VERSION', '1.0')
    API_DESCRIPTION: str = os.getenv('API_DESCRIPTION', 'A simple digital library API with book management and authentication')

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present.
        Returns True if valid, raises ValueError otherwise.
        """
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is required")
        if not cls.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY environment variable is required")
        return True


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False

    @classmethod
    def validate(cls) -> bool:
        """Production requires stronger validation"""
        super().validate()

        # In production, ensure we're not using default credentials
        if cls.ADMIN_PASSWORD == 'password123':
            raise ValueError("Change default admin password in production!")

        return True


class TestConfig(Config):
    """Test environment configuration"""
    DEBUG = True
    PORT = 5002  # Different port for testing


# Configuration factory
def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration based on environment.

    Args:
        env: Environment name ('development', 'production', 'test').
             If None, uses FLASK_ENV or defaults to 'development'

    Returns:
        Appropriate Config subclass
    """
    if env is None:
        env = os.getenv('FLASK_ENV', os.getenv('ENV', 'development'))

    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'test': TestConfig,
    }

    return configs.get(env.lower(), DevelopmentConfig)


# Export the active configuration
config = get_config()
