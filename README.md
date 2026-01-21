# Getting Started

Complete setup guide for the Convert Framework Workshop.

## Prerequisites

### Required Software

**For Everyone:**
- **Git** - Version control
- **VS Code** - Code editor
- **GitHub Copilot** - AI assistant (subscription or trial required)

**For Go Application:**
- **Go 1.21+** - [Download](https://go.dev/dl/)

**For Python Application:**
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **pip** - Included with Python
- **virtualenv** - `pip install virtualenv`

## Quick Setup

### 1. Install GitHub Copilot

1. Open VS Code
2. Install "GitHub Copilot" extension
3. Sign in with your GitHub account
4. Verify Copilot icon is green in status bar

### 2. Clone Repository

```bash
git clone <your-repo-url>
cd convert-framework
```

### 3. Choose Your Path

**Option A: Try Go Application**
```bash
# Install Go dependencies
make setup-go

# Run URL Shortener
make run-url
```

**Option B: Try Python Application**
```bash
# Setup Python environment
make setup-python

# Configure API keys for Weather API
cp python/weather-api/.env.example python/weather-api/.env
# Edit .env and add your API keys

# Run Weather API
make run-weather
# API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

## Detailed Setup

### Go Application Setup

#### URL Shortener

1. **Run the application**
   ```bash
   cd go/url-shortener
   go mod tidy
   go run cmd/server/main.go
   ```

2. **Test it**
   ```bash
   curl -X POST http://localhost:8080/api/urls \
     -H "X-API-Key: test-key" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://github.com"}'
   ```

### Python Application Setup \
### Python Application Setup

#### Weather API

1. **Setup environment**
   ```bash
   cd python/weather-api
   python3 -m venv venv  # Windows: python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Get API keys (Free)**
   - OpenWeatherMap: https://openweathermap.org/api
   - WeatherAPI: https://www.weatherapi.com/

3. **Configure**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run it**
   ```bash
   python main.py
   # Or with auto-reload: uvicorn main:app --reload
   ```

5. **Test it**
   ```bash
   # Open API Documentation in browser
   open http://localhost:8000/docs  # macOS
   # Or visit: http://localhost:8000/docs
   
   # Get current weather
   curl http://localhost:8000/weather/current/Bangkok
   
   # Get forecast
   curl "http://localhost:8000/weather/forecast/Tokyo?days=5"
   
   # Compare multiple cities
   curl -X POST http://localhost:8000/weather/compare \
     -H "Content-Type: application/json" \
     -d '{"locations": ["Bangkok", "Singapore", "Tokyo"]}'
   
   # Manage favorites
   curl http://localhost:8000/favorites
   curl -X POST http://localhost:8000/favorites/Bangkok
   curl http://localhost:8000/favorites/Bangkok
   curl -X DELETE http://localhost:8000/favorites/Bangkok
   
   # Health check
   curl http://localhost:8000/health
   ```

## Verify Your Setup

### Check Go Installation

```bash
go version  # Should show 1.21 or higher
```

### Check Python Installation

```bash
python3 --version  # Should show 3.11 or higher
# Windows users: python --version
```

### Check GitHub Copilot

1. Open any `.go` or `.py` file in VS Code
2. Type a comment: `// Create a function that...`
3. Wait for Copilot suggestion (gray text)
4. If you see suggestions, Copilot is working!

## Usage Examples

### URL Shortener API (Go)

```bash
# Start the server
make run-url
# Server runs on http://localhost:8080

# Shorten a URL
curl -X POST http://localhost:8080/api/urls \
  -H "X-API-Key: test-key" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://github.com/features"}'

# Response:
# {"short_code":"abc123","original_url":"https://github.com/features","created_at":"2026-01-21T..."}

# Use the shortened URL
curl -L http://localhost:8080/abc123
# Redirects to https://github.com/features

# List all shortened URLs
curl http://localhost:8080/api/urls \
  -H "X-API-Key: test-key"

# Get analytics
curl http://localhost:8080/api/analytics/abc123 \
  -H "X-API-Key: test-key"

# Response:
# {"short_code":"abc123","clicks":1,"created_at":"...","last_accessed":"..."}

# Delete a shortened URL
curl -X DELETE http://localhost:8080/api/urls/abc123 \
  -H "X-API-Key: test-key"
```

### Weather API (Python)

```bash
# Start the server
make run-weather
# Server runs on http://localhost:8000

# Get current weather for a city
curl http://localhost:8000/weather/current/Bangkok

# Response:
# {
#   "location": "Bangkok",
#   "avg_temperature": 32.5,
#   "avg_humidity": 70.0,
#   "consensus_description": "Partly cloudy",
#   "sources": [...]
# }

# Get 5-day forecast
curl "http://localhost:8000/weather/forecast/Tokyo?days=5"

# Compare weather across multiple cities
curl -X POST http://localhost:8000/weather/compare \
  -H "Content-Type: application/json" \
  -d '{"locations": ["Bangkok", "Singapore", "Tokyo"]}'

# Add a city to favorites
curl -X POST http://localhost:8000/favorites/Bangkok

# List all favorite cities
curl http://localhost:8000/favorites

# Remove from favorites
curl -X DELETE http://localhost:8000/favorites/Bangkok

# View interactive API docs
open http://localhost:8000/docs
```

## Application Features

### URL Shortener (Go)
- ✅ Create short URLs with custom or auto-generated codes
- ✅ Redirect to original URLs
- ✅ Track click analytics
- ✅ API key authentication
- ✅ SQLite storage
- ✅ In-memory caching
- ✅ RESTful JSON API

### Weather API (Python)
- ✅ Get current weather from WeatherAPI.com
- ✅ Get weather forecasts (1-7 days)
- ✅ Compare weather across multiple cities
- ✅ Manage favorite locations
- ✅ SQLite caching (optional)
- ✅ Interactive API documentation (Swagger UI)
- ✅ RESTful JSON API with FastAPI

## Troubleshooting

### Copilot Not Working

- Check status bar icon (bottom right)
- Reload VS Code: `Cmd/Ctrl + Shift + P` → "Reload Window"
- Sign out and sign in again

### Python Import Errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Go Module Errors

```bash
# Clean module cache
go clean -modcache

# Re-download dependencies
go mod download
```

## Next Steps

Once everything is set up:

1. **Read** [APPLICATION_SELECTION.md](APPLICATION_SELECTION.md) to choose your app
2. **Review** [COPILOT_GUIDE.md](COPILOT_GUIDE.md) for AI techniques
3. **Start converting!** Follow the implementation plan
4. **Track progress** in [WORKSHOP_PROGRESS.md](WORKSHOP_PROGRESS.md)

## Next Steps

Once everything is set up:

1. **Choose your conversion path:**
   - Go → Python: Convert URL Shortener to FastAPI
   - Python → Go: Convert Weather CLI to Cobra

2. **Review guides:**
   - [COPILOT_GUIDE.md](COPILOT_GUIDE.md) for AI techniques
   - [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed specs
   - App-specific READMEs for architecture details

3. **Start converting!** Use GitHub Copilot to assist

4. **Track progress** as you go

## Getting Help

During the workshop:
- Ask the instructor
- Check app-specific README files
- Review Copilot Guide for prompt examples
- Consult Implementation Plan for detailed specs

Happy coding! 🚀
