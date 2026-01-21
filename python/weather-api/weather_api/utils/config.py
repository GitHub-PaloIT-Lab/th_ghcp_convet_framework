"""Configuration utilities"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_config() -> dict:
    """Load configuration from environment"""
    # Load .env file if exists
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
    
    return {
        'weatherapi_key': os.getenv('WEATHERAPI_KEY'),
    }
