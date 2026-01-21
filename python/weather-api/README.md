# Weather API

A REST API to fetch and aggregate weather data from multiple sources with caching and favorites support.

## ⚡ Quick Run

```bash
# 1. Setup environment
python3 -m venv venv  # Windows: python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add:
# WEATHERAPI_KEY=your_key_here

# 3. Start the server
python main.py
# Or with uvicorn: uvicorn main:app --reload

# 4. Access the API
# Documentation: http://localhost:8000/docs
# API: http://localhost:8000/weather/current/Bangkok
```

## 🔑 Get Free API Key

- **WeatherAPI**: https://www.weatherapi.com/ (Free tier: 1M calls/month)

## 🧪 Example Usage

```bash
# Get current weather
curl http://localhost:8000/weather/current/Bangkok

# Get forecast
curl http://localhost:8000/weather/forecast/Tokyo?days=5

# Compare multiple locations
curl -X POST http://localhost:8000/weather/compare \
  -H "Content-Type: application/json" \
  -d '{"locations": ["Bangkok", "Singapore", "Tokyo"]}'

# Manage favorites
curl http://localhost:8000/favorites
curl -X POST http://localhost:8000/favorites/Bangkok
curl -X DELETE http://localhost:8000/favorites/Bangkok
```

## Features

- ✅ RESTful API with FastAPI
- ✅ Fetch weather data from WeatherAPI
- ✅ Current weather and forecast endpoints
- ✅ Cache results to reduce API calls
- ✅ Favorites management
- ✅ Interactive API documentation (Swagger UI)
- ✅ Unit conversion (Celsius/Fahrenheit)

## API Endpoints

### Weather

- **GET** `/weather/current/{location}` - Get current weather
  - Query params: `no_cache` (bool), `units` (metric/imperial)
  
- **GET** `/weather/forecast/{location}` - Get weather forecast
  - Query params: `days` (1-7, default: 5)
  
- **POST** `/weather/compare` - Compare weather across locations
  - Body: `{"locations": ["Bangkok", "Tokyo"]}`

### Favorites

- **GET** `/favorites` - List all favorite locations
- **POST** `/favorites/{location}` - Add location to favorites
- **DELETE** `/favorites/{location}` - Remove from favorites
- **GET** `/favorites/{location}` - Check if location is favorited

### System

- **GET** `/` - API information
- **GET** `/health` - Health check
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - API documentation (ReDoc)

## Installation

1. **Create virtual environment**
   ```bash
   cd python/weather-cli
   python3 -m venv venv  # Windows: python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup API keys**
   Create a `.env` file:
   ```
   WEATHERAPI_KEY=your_key_here
   ```

4. **Run the server**
   ```bash
   python main.py
   # Or with auto-reload: uvicorn main:app --reload
   ```

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (TODO)
pytest

# Format code
black .

# Type checking
mypy weather_cli
```

## Conversion Target

This application is designed to be converted to **Go with Gin or Chi framework**.

### Key Conversion Points:

1. **FastAPI → Gin/Chi**
   - Route definitions
   - Middleware
   - Request/response handling
   - Dependency injection → manual initialization

2. **Pydantic models → Go structs**
   - Request/response schemas → structs with JSON tags
   - Validation → manual validation or validator package

3. **Python async → Go goroutines**
   - `async/await` → goroutines + channels
   - Concurrent API calls → sync.WaitGroup

4. **Exception handling → Error returns**
   - `try/except` → `if err != nil`
   - HTTPException → error responses

5. **SQLite operations**
   - Python code → database/sql or gorm

## Project Structure

```
weather-cli/
├── main.py                 # FastAPI application
├── weather_cli/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py      # Pydantic models
│   │   └── routes/
│   │       ├── weather.py  # Weather endpoints
│   │       └── favorites.py # Favorites endpoints
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
│   └── utils/
│       └── config.py       # Configuration
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Example Response

```json
{
  "location": "Bangkok",
  "avg_temperature": 32.5,
  "avg_humidity": 65.0,
  "consensus_description": "Partly cloudy",
  "sources": [
    {
      "location": "Bangkok",
      "temperature": 32.5,
      "feels_like": 35.2,
      "humidity": 65,
      "description": "Partly cloudy",
      "wind_speed": 15.5,
      "timestamp": "2026-01-21T12:00:00",
      "source": "OpenWeather"
    }
  ]
}
```

## License

This is a workshop example application.
