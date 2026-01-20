"""Main CLI application"""
import click
from weather_cli.weather.aggregator import WeatherAggregator
from weather_cli.weather.openweather import OpenWeatherClient
from weather_cli.weather.weatherapi import WeatherAPIClient
from weather_cli.storage.cache import WeatherCache
from weather_cli.storage.favorites import FavoritesManager
from weather_cli.formatters.table_formatter import TableFormatter
from weather_cli.formatters.json_formatter import JSONFormatter
from weather_cli.formatters.simple_formatter import SimpleFormatter
from weather_cli.utils.config import load_config
import asyncio


@click.group()
@click.pass_context
def cli(ctx):
    """Weather CLI Tool - Get weather data from multiple sources"""
    ctx.ensure_object(dict)
    
    # Load configuration
    config = load_config()
    ctx.obj['config'] = config
    
    # Initialize components
    cache = WeatherCache()
    ctx.obj['cache'] = cache
    
    # Initialize API clients
    clients = []
    if config.get('OPENWEATHER_API_KEY'):
        clients.append(OpenWeatherClient(config['OPENWEATHER_API_KEY']))
    if config.get('WEATHERAPI_KEY'):
        clients.append(WeatherAPIClient(config['WEATHERAPI_KEY']))
    
    ctx.obj['aggregator'] = WeatherAggregator(clients, cache)
    ctx.obj['favorites'] = FavoritesManager()


@cli.command()
@click.argument('location')
@click.option('--format', 'output_format', type=click.Choice(['table', 'json', 'simple']), 
              default='table', help='Output format')
@click.option('--units', type=click.Choice(['metric', 'imperial']), 
              default='metric', help='Temperature units')
@click.option('--no-cache', is_flag=True, help='Disable cache')
@click.pass_context
def current(ctx, location: str, output_format: str, units: str, no_cache: bool):
    """Get current weather for a location"""
    aggregator = ctx.obj['aggregator']
    
    # Fetch weather data
    weather = asyncio.run(aggregator.get_current_weather(location, use_cache=not no_cache))
    
    if not weather:
        click.echo(f"❌ Could not fetch weather data for {location}", err=True)
        return
    
    # Format and display
    formatter = _get_formatter(output_format)
    output = formatter.format_current(weather, units)
    click.echo(output)


@cli.command()
@click.argument('location')
@click.option('--days', type=int, default=5, help='Number of days to forecast')
@click.option('--format', 'output_format', type=click.Choice(['table', 'json', 'simple']), 
              default='table', help='Output format')
@click.pass_context
def forecast(ctx, location: str, days: int, output_format: str):
    """Get weather forecast"""
    aggregator = ctx.obj['aggregator']
    
    # Fetch forecast data
    forecast_data = asyncio.run(aggregator.get_forecast(location, days))
    
    if not forecast_data:
        click.echo(f"❌ Could not fetch forecast for {location}", err=True)
        return
    
    # Format and display
    formatter = _get_formatter(output_format)
    output = formatter.format_forecast(forecast_data)
    click.echo(output)


@cli.command()
@click.argument('location')
@click.pass_context
def add_favorite(ctx, location: str):
    """Add a location to favorites"""
    favorites = ctx.obj['favorites']
    
    try:
        favorites.add(location)
        click.echo(f"✅ Added '{location}' to favorites")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)


@cli.command()
@click.argument('location')
@click.pass_context
def remove_favorite(ctx, location: str):
    """Remove a location from favorites"""
    favorites = ctx.obj['favorites']
    
    if favorites.remove(location):
        click.echo(f"✅ Removed '{location}' from favorites")
    else:
        click.echo(f"❌ '{location}' not found in favorites", err=True)


@cli.command()
@click.pass_context
def list_favorites(ctx):
    """List all favorite locations"""
    favorites = ctx.obj['favorites']
    locations = favorites.list()
    
    if not locations:
        click.echo("No favorite locations saved")
        return
    
    click.echo("📍 Favorite Locations:")
    for location in locations:
        click.echo(f"  • {location}")


@cli.command()
@click.argument('locations', nargs=-1, required=True)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), 
              default='table', help='Output format')
@click.pass_context
def compare(ctx, locations: tuple, output_format: str):
    """Compare weather across multiple locations"""
    aggregator = ctx.obj['aggregator']
    
    # Fetch weather for all locations
    weather_data = []
    for location in locations:
        weather = asyncio.run(aggregator.get_current_weather(location, use_cache=True))
        if weather:
            weather_data.append(weather)
    
    if not weather_data:
        click.echo("❌ Could not fetch weather data for any location", err=True)
        return
    
    # Format and display comparison
    formatter = _get_formatter(output_format)
    output = formatter.format_comparison(weather_data)
    click.echo(output)


@cli.command()
@click.pass_context
def clear_cache(ctx):
    """Clear the weather cache"""
    cache = ctx.obj['cache']
    cache.clear_expired()
    click.echo("✅ Cache cleared")


def _get_formatter(format_type: str):
    """Get the appropriate formatter"""
    formatters = {
        'table': TableFormatter(),
        'json': JSONFormatter(),
        'simple': SimpleFormatter(),
    }
    return formatters.get(format_type, TableFormatter())


if __name__ == '__main__':
    cli()
