"""API response models"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class WeatherDataResponse(BaseModel):
    """Weather data response model"""
    location: str
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Feels like temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    description: str
    wind_speed: float = Field(..., description="Wind speed in km/h")
    timestamp: datetime
    source: str = Field(..., description="API source name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Bangkok",
                "temperature": 32.5,
                "feels_like": 35.2,
                "humidity": 70,
                "description": "Partly cloudy",
                "wind_speed": 15.5,
                "timestamp": "2026-01-21T12:00:00",
                "source": "OpenWeather"
            }
        }


class AggregatedWeatherResponse(BaseModel):
    """Aggregated weather response model"""
    location: str
    avg_temperature: float = Field(..., description="Average temperature in Celsius")
    avg_humidity: float = Field(..., description="Average humidity percentage")
    consensus_description: str = Field(..., description="Most common weather description")
    sources: List[WeatherDataResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Bangkok",
                "avg_temperature": 32.0,
                "avg_humidity": 68.5,
                "consensus_description": "Partly cloudy",
                "sources": [
                    {
                        "location": "Bangkok",
                        "temperature": 32.5,
                        "feels_like": 35.2,
                        "humidity": 70,
                        "description": "Partly cloudy",
                        "wind_speed": 15.5,
                        "timestamp": "2026-01-21T12:00:00",
                        "source": "OpenWeather"
                    }
                ]
            }
        }


class ForecastResponse(BaseModel):
    """Forecast response model"""
    location: str
    forecast: List[WeatherDataResponse]
    days: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Tokyo",
                "days": 5,
                "forecast": []
            }
        }


class CompareRequest(BaseModel):
    """Weather comparison request"""
    locations: List[str] = Field(..., min_length=2, max_length=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "locations": ["Bangkok", "Singapore", "Tokyo"]
            }
        }


class CompareResponse(BaseModel):
    """Weather comparison response"""
    comparison: List[AggregatedWeatherResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "comparison": []
            }
        }


class FavoriteResponse(BaseModel):
    """Favorite location response"""
    location: str
    added_at: Optional[datetime] = None


class FavoritesListResponse(BaseModel):
    """List of favorite locations"""
    favorites: List[str]
    count: int


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Not Found",
                "detail": "Location not found"
            }
        }
