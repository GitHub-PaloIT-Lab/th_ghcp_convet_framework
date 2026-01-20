"""JSON output formatter"""
import json
from weather_cli.models import AggregatedWeather, WeatherData


class JSONFormatter:
    """Format weather data as JSON"""
    
    def format_current(self, weather: AggregatedWeather, units: str = 'metric') -> str:
        """Format current weather"""
        data = weather.to_dict()
        if units == 'imperial':
            data['avg_temperature'] = (data['avg_temperature'] * 9/5) + 32
            data['unit'] = 'fahrenheit'
        else:
            data['unit'] = 'celsius'
        return json.dumps(data, indent=2)
    
    def format_forecast(self, forecast: list[WeatherData]) -> str:
        """Format forecast data"""
        data = [w.to_dict() for w in forecast]
        return json.dumps(data, indent=2)
    
    def format_comparison(self, weather_list: list[AggregatedWeather]) -> str:
        """Format weather comparison"""
        data = [w.to_dict() for w in weather_list]
        return json.dumps(data, indent=2)


class SimpleFormatter:
    """Simple text output formatter"""
    
    def format_current(self, weather: AggregatedWeather, units: str = 'metric') -> str:
        """Format current weather"""
        temp = weather.avg_temperature
        if units == 'imperial':
            temp = (temp * 9/5) + 32
            unit = '°F'
        else:
            unit = '°C'
        
        return f"""
🌤️  {weather.location}
🌡️  {temp:.1f}{unit}
💧 {weather.avg_humidity}% humidity
☁️  {weather.consensus_description}
📊 Data from {len(weather.sources)} source(s)
"""
    
    def format_forecast(self, forecast: list[WeatherData]) -> str:
        """Format forecast data"""
        lines = ["📅 Weather Forecast:\n"]
        for weather in forecast:
            lines.append(
                f"  {weather.timestamp.strftime('%Y-%m-%d')}: "
                f"{weather.temperature:.1f}°C - {weather.description}"
            )
        return "\n".join(lines)
    
    def format_comparison(self, weather_list: list[AggregatedWeather]) -> str:
        """Format weather comparison"""
        lines = ["🌍 Weather Comparison:\n"]
        for weather in weather_list:
            lines.append(
                f"  {weather.location}: {weather.avg_temperature:.1f}°C, "
                f"{weather.consensus_description}"
            )
        return "\n".join(lines)
