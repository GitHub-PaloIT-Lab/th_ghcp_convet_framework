"""WeatherAPI.com client"""
from datetime import datetime
from weather_cli.weather import WeatherAPIClient
from weather_cli.models import WeatherData


class WeatherAPIClient(WeatherAPIClient):
    """WeatherAPI.com implementation"""
    BASE_URL = "https://api.weatherapi.com/v1"
    
    async def get_current_weather(self, location: str) -> WeatherData:
        """Fetch current weather from WeatherAPI.com"""
        url = f"{self.BASE_URL}/current.json"
        params = {
            'key': self.api_key,
            'q': location
        }
        
        try:
            data = self._make_request(url, params)
            return self._parse_current(data)
        except Exception as e:
            raise RuntimeError(f"WeatherAPI error: {e}") from e
    
    async def get_forecast(self, location: str, days: int) -> list[WeatherData]:
        """Fetch forecast from WeatherAPI.com"""
        url = f"{self.BASE_URL}/forecast.json"
        params = {
            'key': self.api_key,
            'q': location,
            'days': days
        }
        
        try:
            data = self._make_request(url, params)
            return [self._parse_forecast_day(day, location) for day in data['forecast']['forecastday']]
        except Exception as e:
            raise RuntimeError(f"WeatherAPI forecast error: {e}") from e
    
    def _parse_current(self, data: dict) -> WeatherData:
        """Parse current weather response"""
        return WeatherData(
            location=data['location']['name'],
            temperature=data['current']['temp_c'],
            feels_like=data['current']['feelslike_c'],
            humidity=data['current']['humidity'],
            description=data['current']['condition']['text'],
            wind_speed=data['current']['wind_kph'],
            timestamp=datetime.now(),
            source='WeatherAPI.com'
        )
    
    def _parse_forecast_day(self, day: dict, location: str) -> WeatherData:
        """Parse forecast day"""
        return WeatherData(
            location=location,
            temperature=day['day']['avgtemp_c'],
            feels_like=day['day']['avgtemp_c'],
            humidity=day['day']['avghumidity'],
            description=day['day']['condition']['text'],
            wind_speed=day['day']['maxwind_kph'],
            timestamp=datetime.strptime(day['date'], '%Y-%m-%d'),
            source='WeatherAPI.com'
        )
