"""Weather API routes"""
from fastapi import APIRouter, HTTPException, Query, Path, Request
from typing import List

from weather_api.api.schemas import (
    AggregatedWeatherResponse,
    ForecastResponse,
    CompareRequest,
    CompareResponse,
    WeatherDataResponse
)
from weather_api.models import AggregatedWeather, WeatherData


router = APIRouter()


def get_aggregator(request: Request):
    """Get aggregator from app state"""
    aggregator = request.app.state.aggregator
    if not aggregator:
        raise HTTPException(status_code=500, detail="Weather service not initialized")
    return aggregator


def convert_weather_data(data: WeatherData) -> WeatherDataResponse:
    """Convert internal model to API response"""
    return WeatherDataResponse(
        location=data.location,
        temperature=data.temperature,
        feels_like=data.feels_like,
        humidity=data.humidity,
        description=data.description,
        wind_speed=data.wind_speed,
        timestamp=data.timestamp,
        source=data.source
    )


def convert_aggregated_weather(data: AggregatedWeather) -> AggregatedWeatherResponse:
    """Convert internal aggregated model to API response"""
    return AggregatedWeatherResponse(
        location=data.location,
        avg_temperature=data.avg_temperature,
        avg_humidity=data.avg_humidity,
        consensus_description=data.consensus_description,
        sources=[convert_weather_data(s) for s in data.sources]
    )


@router.get(
    "/current/{location}",
    response_model=AggregatedWeatherResponse,
    summary="Get current weather",
    description="Get current weather data for a location from multiple sources"
)
async def get_current_weather(
    request: Request,
    location: str = Path(..., description="Location name (city, country, etc.)"),
    no_cache: bool = Query(False, description="Skip cache and fetch fresh data"),
    units: str = Query("metric", enum=["metric", "imperial"], description="Temperature units")
):
    """Get current weather for a location"""
    aggregator = get_aggregator(request)
    
    try:
        weather = await aggregator.get_current_weather(location, use_cache=False)  # Disable cache
        
        if not weather:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch weather data for '{location}'"
            )
        
        response = convert_aggregated_weather(weather)
        
        # Convert to imperial if requested
        if units == "imperial":
            response.avg_temperature = (response.avg_temperature * 9/5) + 32
            for source in response.sources:
                source.temperature = (source.temperature * 9/5) + 32
                source.feels_like = (source.feels_like * 9/5) + 32
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/forecast/{location}",
    response_model=ForecastResponse,
    summary="Get weather forecast",
    description="Get weather forecast for a location"
)
async def get_forecast(
    request: Request,
    location: str = Path(..., description="Location name"),
    days: int = Query(5, ge=1, le=7, description="Number of days to forecast")
):
    """Get weather forecast for a location"""
    aggregator = get_aggregator(request)
    
    try:
        forecast_data = await aggregator.get_forecast(location, days)
        
        if not forecast_data:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch forecast for '{location}'"
            )
        
        return ForecastResponse(
            location=location,
            days=days,
            forecast=[convert_weather_data(f) for f in forecast_data]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/compare",
    response_model=CompareResponse,
    summary="Compare weather across locations",
    description="Get and compare weather data for multiple locations"
)
async def compare_weather(request: Request, compare_request: CompareRequest):
    """Compare weather across multiple locations"""
    aggregator = get_aggregator(request)
    
    try:
        comparison = []
        
        for location in compare_request.locations:
            weather = await aggregator.get_current_weather(location, use_cache=False)  # Disable cache
            if weather:
                comparison.append(convert_aggregated_weather(weather))
        
        if not comparison:
            raise HTTPException(
                status_code=404,
                detail="Could not fetch weather data for any location"
            )
        
        return CompareResponse(comparison=comparison)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
