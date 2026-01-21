"""Base API client"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import requests
from weather_api.models import WeatherData

class WeatherAPIClient(ABC):
    """Base class for weather API clients"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
    
    @abstractmethod
    async def get_current_weather(self, location: str) -> WeatherData:
        """Fetch current weather for a location"""
        pass
    
    @abstractmethod
    async def get_forecast(self, location: str, days: int) -> list[WeatherData]:
        """Fetch weather forecast"""
        pass
    
    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to API"""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e
