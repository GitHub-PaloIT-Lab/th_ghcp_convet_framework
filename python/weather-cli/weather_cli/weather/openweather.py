"""OpenWeatherMap API client"""
from datetime import datetime
from weather_cli.weather import WeatherAPIClient
from weather_cli.models import WeatherData


class OpenWeatherClient(WeatherAPIClient):
    """OpenWeatherMap API implementation"""
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, location: str) -> WeatherData:
        """Fetch current weather from OpenWeatherMap"""
        url = f"{self.BASE_URL}/weather"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            data = self._make_request(url, params)
            return self._parse_current(data)
        except Exception as e:
            raise RuntimeError(f"OpenWeather API error: {e}") from e
    
    async def get_forecast(self, location: str, days: int) -> list[WeatherData]:
        """Fetch forecast from OpenWeatherMap"""
        url = f"{self.BASE_URL}/forecast"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        try:
            data = self._make_request(url, params)
            return [self._parse_forecast_item(item, location) for item in data['list'][:days]]
        except Exception as e:
            raise RuntimeError(f"OpenWeather forecast error: {e}") from e
    
    def _parse_current(self, data: dict) -> WeatherData:
        """Parse current weather response"""
        return WeatherData(
            location=data['name'],
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            humidity=data['main']['humidity'],
            description=data['weather'][0]['description'],
            wind_speed=data['wind']['speed'] * 3.6,  # m/s to km/h
            timestamp=datetime.now(),
            source='OpenWeatherMap'
        )
    
    def _parse_forecast_item(self, item: dict, location: str) -> WeatherData:
        """Parse forecast item"""
        return WeatherData(
            location=location,
            temperature=item['main']['temp'],
            feels_like=item['main']['feels_like'],
            humidity=item['main']['humidity'],
            description=item['weather'][0]['description'],
            wind_speed=item['wind']['speed'] * 3.6,
            timestamp=datetime.fromtimestamp(item['dt']),
            source='OpenWeatherMap'
        )
