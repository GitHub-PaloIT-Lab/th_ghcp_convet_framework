# Getting Started

Complete setup guide for the Convert Framework Workshop.

## Prerequisites

### Required Software

**For Everyone:**
- **Git** - Version control
- **VS Code** - Code editor
- **GitHub Copilot** - AI assistant (subscription or trial required)

**For Go Applications:**
- **Go 1.21+** - [Download](https://go.dev/dl/)
- **Redis** - For URL Shortener only
  - macOS: `brew install redis`
  - Linux: `apt install redis-server`
  - Windows: Use Docker or WSL2

**For Python Applications:**
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

**Option A: Try Go Applications**
```bash
# Install Go dependencies
make setup-go

# Start Redis (for URL Shortener)
redis-server &

# Run URL Shortener
make run-url
```

**Option B: Try Python Applications**
```bash
# Setup Python environments
make setup-python

# Configure API keys for Weather CLI
cp python/weather-cli/.env.example python/weather-cli/.env
# Edit .env and add your API keys

# Run Weather CLI
make run-weather
```

## Detailed Setup

### Go Applications Setup

#### URL Shortener

1. **Install Redis**
   ```bash
   # macOS
   brew install redis
   brew services start redis
   
   # Linux
   sudo apt install redis-server
   sudo systemctl start redis
   
   # Docker
   docker run -d -p 6379:6379 redis
   ```

2. **Run the application**
   ```bash
   cd go/url-shortener
   go mod download
   go run cmd/server/main.go
   ```

3. **Test it**
   ```bash
   curl -X POST http://localhost:8080/api/shorten \
     -H "X-API-Key: test-key" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://github.com"}'
   ```

#### Blog API

1. **Run the application**
   ```bash
   cd go/blog-api
   go mod download
   go run cmd/server/main.go
   ```

2. **Test it**
   ```bash
   # Register a user
   curl -X POST http://localhost:8080/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"test","email":"test@example.com","password":"pass123"}'
   ```

### Python Applications Setup

#### Weather CLI

1. **Setup environment**
   ```bash
   cd python/weather-cli
   python -m venv venv
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

4. **Use it**
   ```bash
   python -m weather_cli.cli current "Bangkok"
   python -m weather_cli.cli forecast "Tokyo" --days 5
   ```

#### Web Scraper

1. **Setup environment**
   ```bash
   cd python/web-scraper
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Use it**
   ```bash
   python -m web_scraper.cli \
     --config examples/hacker_news.json \
     --output results.json
   ```

## Verify Your Setup

### Check Go Installation

```bash
go version  # Should show 1.21 or higher
```

### Check Python Installation

```bash
python --version  # Should show 3.11 or higher
```

### Check Redis (if needed)

```bash
redis-cli ping  # Should return "PONG"
```

### Check GitHub Copilot

1. Open any `.go` or `.py` file in VS Code
2. Type a comment: `// Create a function that...`
3. Wait for Copilot suggestion (gray text)
4. If you see suggestions, Copilot is working!

## Troubleshooting

### Copilot Not Working

- Check status bar icon (bottom right)
- Reload VS Code: `Cmd/Ctrl + Shift + P` → "Reload Window"
- Sign out and sign in again

### Redis Connection Error

```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server
```

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

## Getting Help

During the workshop:
- Ask the instructor
- Check app-specific README files
- Review Copilot Guide for prompt examples
- Consult Implementation Plan for detailed specs

Happy coding! 🚀
