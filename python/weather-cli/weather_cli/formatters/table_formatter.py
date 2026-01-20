"""Table output formatter"""
from tabulate import tabulate
from weather_cli.models import AggregatedWeather, WeatherData


class TableFormatter:
    """Format weather data as table"""
    
    def format_current(self, weather: AggregatedWeather, units: str = 'metric') -> str:
        """Format current weather"""
        temp = weather.avg_temperature
        if units == 'imperial':
            temp = (temp * 9/5) + 32
            unit_symbol = '°F'
        else:
            unit_symbol = '°C'
        
        table = [
            ['Location', weather.location],
            ['Temperature', f"{temp:.1f}{unit_symbol}"],
            ['Humidity', f"{weather.avg_humidity}%"],
            ['Condition', weather.consensus_description],
            ['Sources', len(weather.sources)],
        ]
        
        return tabulate(table, tablefmt='grid')
    
    def format_forecast(self, forecast: list[WeatherData]) -> str:
        """Format forecast data"""
        headers = ['Date', 'Temperature', 'Condition']
        rows = []
        
        for weather in forecast:
            rows.append([
                weather.timestamp.strftime('%Y-%m-%d'),
                f"{weather.temperature:.1f}°C",
                weather.description
            ])
        
        return tabulate(rows, headers=headers, tablefmt='grid')
    
    def format_comparison(self, weather_list: list[AggregatedWeather]) -> str:
        """Format weather comparison"""
        headers = ['Location', 'Temp (°C)', 'Humidity', 'Condition']
        rows = []
        
        for weather in weather_list:
            rows.append([
                weather.location,
                f"{weather.avg_temperature:.1f}",
                f"{weather.avg_humidity}%",
                weather.consensus_description
            ])
        
        return tabulate(rows, headers=headers, tablefmt='grid')
