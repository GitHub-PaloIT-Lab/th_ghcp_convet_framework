.PHONY: help run-url run-weather setup-go setup-python clean

# Detect Python command (python3 on Unix/macOS, python on Windows)
PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null || echo python)

help:
	@echo "Convert Framework Workshop - Quick Commands"
	@echo ""
	@echo "Running Applications:"
	@echo "  make run-url       Run Go URL Shortener API"
	@echo "  make run-weather   Run Python Weather API"
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
	@echo "🌤️  Starting Weather API at http://localhost:8000"
	@echo "📚 Documentation: http://localhost:8000/docs"
	@cd python/weather-api && venv/bin/python main.py

# Setup
setup-go:
	@echo "📦 Installing Go dependencies..."
	cd go/url-shortener && go mod tidy
	@echo "✅ Go dependencies installed"

setup-python:
	@echo "🐍 Setting up Python environment..."
	cd python/weather-api && $(PYTHON) -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Python environment ready"
	@echo ""
	@echo "⚠️  Don't forget to configure API keys:"
	@echo "  cp python/weather-api/.env.example python/weather-api/.env"
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
