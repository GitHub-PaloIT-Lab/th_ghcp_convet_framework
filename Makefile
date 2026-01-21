.PHONY: help run-url run-weather setup-go setup-python clean

help:
	@echo "Convert Framework Workshop - Quick Commands"
	@echo ""
	@echo "Running Applications:"
	@echo "  make run-url       Run Go URL Shortener"
	@echo "  make run-weather   Run Python Weather CLI (interactive)"
	@echo ""
	@echo "Setup:"
	@echo "  make setup-go      Install Go dependencies"
	@echo "  make setup-python  Setup Python virtual environment"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         Clean build artifacts and caches"
	@echo ""

# Go Applications
run-url:
	@echo "🚀 Starting URL Shortener..."
	@cd go/url-shortener && go mod tidy && go run cmd/server/main.go

# Python Applications  
run-weather:
	@echo "🌤️  Weather CLI Tool"
	@echo ""
	@echo "Available commands:"
	@echo "  python -m weather_cli.cli current \"Bangkok\""
	@echo "  python -m weather_cli.cli forecast \"Tokyo\" --days 5"
	@echo "  python -m weather_cli.cli compare \"Bangkok\" \"Singapore\""
	@echo ""
	@cd python/weather-cli && \
	if [ ! -d "venv" ]; then \
		echo "Setting up virtual environment..."; \
		python -m venv venv; \
		. venv/bin/activate && pip install -r requirements.txt; \
	fi && \
	. venv/bin/activate && python -m weather_cli.cli --help
	@echo "  python -m web_scraper.cli -c examples/hacker_news.json -o results.csv --format csv"
	@echo ""
	@cd python/web-scraper && \
	if [ ! -d "venv" ]; then \
		echo "Setting up virtual environment..."; \
		python -m venv venv; \
		. venv/bin/activate && pip install -r requirements.txt; \
	fi && \
	. venv/bin/activate && python -m web_scraper.cli --help

# Setup
setup-go:
	@echo "📦 Installing Go dependencies..."
	cd go/url-shortener && go mod tidy
	@echo "✅ Go dependencies installed"

setup-python:
	@echo "🐍 Setting up Python environment..."
	cd python/weather-cli && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Python environment ready"
	@echo ""
	@echo "⚠️  Don't forget to configure API keys:"
	@echo "  cp python/weather-cli/.env.example python/weather-cli/.env"
	@echo "  # Edit .env and add your API keys"

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.db" -delete 2>/dev/null || true
	find . -name "*.db-journal" -delete 2>/dev/null || true
	@echo "✅ Cleaned"
