"""Weather API - FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional

from weather_api.api.routes import weather, favorites
from weather_api.utils.config import load_config
from weather_api.storage.cache import WeatherCache
from weather_api.storage.favorites import FavoritesManager
from weather_api.weather.aggregator import WeatherAggregator
from weather_api.weather.weatherapi import WeatherAPIClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application"""
    # Startup: Initialize components
    config = load_config()
    cache = WeatherCache()
    favorites_manager = FavoritesManager()
    
    # Initialize API client (WeatherAPI only)
    clients = []
    if config.get('weatherapi_key'):
        clients.append(WeatherAPIClient(config['weatherapi_key']))
    
    if not clients:
        print("⚠️  Warning: No API keys configured. Please set API keys in .env file")
    
    aggregator = WeatherAggregator(clients, cache)
    
    # Store in app.state
    app.state.config = config
    app.state.cache = cache
    app.state.favorites = favorites_manager
    app.state.aggregator = aggregator
    
    yield
    
    # Shutdown: Cleanup if needed
    pass


# Create FastAPI application
app = FastAPI(
    title="Weather API",
    description="Aggregated weather data from multiple sources",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Weather API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "current_weather": "/weather/current/{location}",
            "forecast": "/weather/forecast/{location}",
            "compare": "/weather/compare",
            "favorites": "/favorites"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    api_clients_count = len(app.state.aggregator.clients) if hasattr(app.state, 'aggregator') and app.state.aggregator else 0
    
    return {
        "status": "healthy",
        "api_clients": api_clients_count,
        "cache_enabled": True
    }


# Include routers
app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(favorites.router, prefix="/favorites", tags=["favorites"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
