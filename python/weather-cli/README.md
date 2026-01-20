# Weather CLI Tool

A command-line tool to fetch and display weather data from multiple sources with caching and favorites support.

## ⚡ Quick Run

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add:
# OPENWEATHER_API_KEY=your_key_here
# WEATHERAPI_KEY=your_key_here

# 3. Use it!
python -m weather_cli.cli current "Bangkok"
python -m weather_cli.cli forecast "Tokyo" --days 5
python -m weather_cli.cli compare "Bangkok" "Singapore" "Tokyo"
```

## 🔑 Get Free API Keys

- **OpenWeatherMap**: https://openweathermap.org/api (Free tier: 1000 calls/day)
- **WeatherAPI**: https://www.weatherapi.com/ (Free tier: 1M calls/month)

## 🧪 Example Output

```
$ python -m weather_cli.cli current "Bangkok"
┌──────────────┬──────────────────┐
│ Location     │ Bangkok          │
├──────────────┼──────────────────┤
│ Temperature  │ 32.5°C           │
├──────────────┼──────────────────┤
│ Humidity     │ 65%              │
├──────────────┼──────────────────┤
│ Condition    │ Partly cloudy    │
└──────────────┴──────────────────┘
```

## Features

- ✅ Fetch weather data from multiple APIs (OpenWeatherMap, WeatherAPI.com)
- ✅ Display current weather and forecast
- ✅ Support multiple output formats (table, JSON, simple)
- ✅ Cache results to reduce API calls
- ✅ Store favorite locations
- ✅ Compare weather across locations
- ✅ Unit conversion (Celsius/Fahrenheit, km/h, mi/h)

## Installation

1. **Create virtual environment**
   ```bash
   cd python/weather-cli
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup API keys**
   Create a `.env` file:
   ```
   OPENWEATHER_API_KEY=your_key_here
   WEATHERAPI_KEY=your_key_here
   ```

## Usage

### Get Current Weather
```bash
weather current "Bangkok"
weather current "Bangkok" --format json
weather current "Bangkok" --units imperial
weather current "Tokyo" --no-cache
```

### Get Forecast
```bash
weather forecast "Bangkok" --days 5
weather forecast "Tokyo" --days 7 --format json
```

### Manage Favorites
```bash
weather add-favorite "Bangkok"
weather list-favorites
weather remove-favorite "Bangkok"
```

### Compare Locations
```bash
weather compare "Bangkok" "Tokyo" "New York"
weather compare "Bangkok" "Singapore" --format json
```

### Utilities
```bash
weather clear-cache
```

## Commands

- `current LOCATION` - Get current weather
- `forecast LOCATION` - Get weather forecast
- `add-favorite LOCATION` - Add to favorites
- `remove-favorite LOCATION` - Remove from favorites
- `list-favorites` - List all favorites
- `compare LOCATIONS...` - Compare weather
- `clear-cache` - Clear weather cache

## Output Formats

- `table` (default) - Formatted table output
- `json` - JSON format
- `simple` - Simple text format

## Conversion Target

This application is designed to be converted to **Go with Cobra CLI framework**.

### Key Conversion Points:

1. **Click framework → Cobra**
   - Commands and subcommands
   - Flags and arguments
   - Command grouping

2. **Python classes → Go structs**
   - API clients → interfaces + structs
   - Data models → structs with methods
   - Aggregator → struct with methods

3. **Async operations → Goroutines**
   - `async/await` → goroutines + channels
   - Concurrent API calls → goroutine synchronization

4. **Exception handling → Error returns**
   - `try/except` → `if err != nil`
   - Custom exceptions → custom error types

5. **SQLite operations**
   - Python sqlite3 → database/sql
   - Context managers → defer

## Project Structure

```
weather-cli/
├── weather_cli/
│   ├── __init__.py
│   ├── cli.py              # Main CLI
│   ├── models/
│   │   └── __init__.py     # Data models
│   ├── weather/
│   │   ├── __init__.py     # Base client
│   │   ├── openweather.py  # OpenWeather client
│   │   ├── weatherapi.py   # WeatherAPI client
│   │   └── aggregator.py   # Data aggregator
│   ├── storage/
│   │   ├── cache.py        # SQLite cache
│   │   └── favorites.py    # Favorites manager
│   ├── formatters/
│   │   ├── table_formatter.py
│   │   └── json_formatter.py
│   └── utils/
│       └── config.py       # Configuration
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Example Output

```
┌──────────────┬──────────────────┐
│ Location     │ Bangkok          │
├──────────────┼──────────────────┤
│ Temperature  │ 32.5°C           │
├──────────────┼──────────────────┤
│ Humidity     │ 65%              │
├──────────────┼──────────────────┤
│ Condition    │ Partly cloudy    │
├──────────────┼──────────────────┤
│ Sources      │ 2                │
└──────────────┴──────────────────┘
```

## License

This is a workshop example application.
