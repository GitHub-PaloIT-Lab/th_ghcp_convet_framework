"""Data models for weather information"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeatherData:
    """Weather data model"""
    location: str
    temperature: float  # Celsius
    feels_like: float
    humidity: int  # Percentage
    description: str
    wind_speed: float  # km/h
    timestamp: datetime
    source: str  # API source name
    
    def to_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit"""
        return (self.temperature * 9/5) + 32
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'location': self.location,
            'temperature': self.temperature,
            'feels_like': self.feels_like,
            'humidity': self.humidity,
            'description': self.description,
            'wind_speed': self.wind_speed,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
        }


@dataclass
class AggregatedWeather:
    """Aggregated weather data from multiple sources"""
    location: str
    avg_temperature: float
    avg_humidity: float
    sources: list[WeatherData]
    consensus_description: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'location': self.location,
            'avg_temperature': self.avg_temperature,
            'avg_humidity': self.avg_humidity,
            'consensus_description': self.consensus_description,
            'sources': [s.to_dict() for s in self.sources],
        }
