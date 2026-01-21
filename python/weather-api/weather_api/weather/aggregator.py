"""Weather data aggregator"""
from typing import List, Optional
from weather_api.weather import WeatherAPIClient
from weather_api.models import WeatherData, AggregatedWeather
from weather_api.storage.cache import WeatherCache
from collections import Counter


class WeatherAggregator:
    """Aggregate weather data from multiple sources"""
    
    def __init__(self, clients: List[WeatherAPIClient], cache: WeatherCache):
        self.clients = clients
        self.cache = cache
    
    async def get_current_weather(self, location: str, use_cache: bool = True) -> Optional[AggregatedWeather]:
        """Get weather from all sources and aggregate"""
        # Try cache first
        if use_cache:
            cached = self.cache.get(location)
            if cached:
                return cached
        
        # Fetch from all sources
        data_list = []
        for client in self.clients:
            try:
                weather = await client.get_current_weather(location)
                data_list.append(weather)
            except Exception as e:
                print(f"Warning: {client.__class__.__name__} failed: {e}")
        
        if not data_list:
            return None
        
        # Aggregate data
        aggregated = self._aggregate_data(data_list)
        
        # Cache result
        if use_cache:
            self.cache.set(location, aggregated)
        
        return aggregated
    
    async def get_forecast(self, location: str, days: int) -> Optional[list[WeatherData]]:
        """Get forecast from the first available source"""
        for client in self.clients:
            try:
                return await client.get_forecast(location, days)
            except Exception as e:
                print(f"Warning: {client.__class__.__name__} forecast failed: {e}")
        return None
    
    def _aggregate_data(self, data_list: List[WeatherData]) -> AggregatedWeather:
        """Aggregate data from multiple sources (average, consensus)"""
        avg_temp = sum(d.temperature for d in data_list) / len(data_list)
        avg_humidity = sum(d.humidity for d in data_list) / len(data_list)
        
        # Find most common description
        descriptions = [d.description for d in data_list]
        consensus_desc = Counter(descriptions).most_common(1)[0][0]
        
        return AggregatedWeather(
            location=data_list[0].location,
            avg_temperature=round(avg_temp, 1),
            avg_humidity=round(avg_humidity, 1),
            sources=data_list,
            consensus_description=consensus_desc
        )
