# URL Shortener API

A RESTful API for shortening URLs with analytics tracking, built with Go, Chi router, Redis cache, and SQLite database.

## ⚡ Quick Run

```bash
# 1. Install dependencies
go mod download

# 2. Start Redis (required)
redis-server
# OR with Docker:
docker run -d -p 6379:6379 redis

# 3. Run the server
go run cmd/server/main.go
# → Server starts at http://localhost:8080
```

## 🧪 Test It

```bash
# Create a short URL
curl -X POST http://localhost:8080/api/shorten \
  -H "X-API-Key: test-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}'

# Response: {"short_code":"abc123","short_url":"http://localhost:8080/abc123"}

# Use the short URL (redirects to original)
curl -L http://localhost:8080/abc123

# Get analytics
curl http://localhost:8080/api/analytics/abc123 \
  -H "X-API-Key: test-key"

# List all URLs
curl http://localhost:8080/api/urls \
  -H "X-API-Key: test-key"
```

## Features

- ✅ Shorten long URLs to unique short codes
- ✅ Redirect from short URL to original URL
- ✅ Track click analytics (count, timestamps, referrers)
- ✅ List all shortened URLs for a user
- ✅ Delete shortened URLs
- ✅ In-memory cache with Redis for fast lookups
- ✅ API key authentication

## Tech Stack

- **Go 1.21+**
- **Chi** - HTTP router
- **Redis** - Caching layer
- **SQLite** - Database
- **go-redis** - Redis client

## Project Structure

```
url-shortener/
├── cmd/
│   └── server/
│       └── main.go           # Entry point
├── internal/
│   ├── handler/
│   │   ├── url_handler.go    # URL HTTP handlers
│   │   ├── analytics_handler.go
│   │   ├── middleware.go     # Authentication
│   │   └── response.go       # Response helpers
│   ├── service/
│   │   ├── url_service.go    # Business logic
│   │   └── analytics_service.go
│   ├── storage/
│   │   ├── cache.go          # Redis cache
│   │   └── sqlite_store.go   # SQLite database
│   └── models/
│       ├── url.go            # Data models
│       └── analytics.go
├── go.mod
├── go.sum
└── README.md
```

## Prerequisites

- Go 1.21 or higher
- Redis server running on `localhost:6379` (or configure `REDIS_ADDR`)

## Installation

1. **Clone the repository**
   ```bash
   cd go/url-shortener
   ```

2. **Install dependencies**
   ```bash
   go mod download
   ```

3. **Start Redis** (if not running)
   ```bash
   redis-server
   ```

4. **Run the server**
   ```bash
   go run cmd/server/main.go
   ```

   The server will start on `http://localhost:8080`

## API Endpoints

### Create Short URL
```http
POST /api/urls
X-API-Key: your-api-key

{
  "original_url": "https://example.com/very/long/url"
}
```

**Response**:
```json
{
  "short_code": "abc123XY",
  "short_url": "http://localhost:8080/abc123XY",
  "original_url": "https://example.com/very/long/url"
}
```

### Redirect to Original URL
```http
GET /{shortCode}
```

Redirects to the original URL and records a click event.

### List User's URLs
```http
GET /api/urls
X-API-Key: your-api-key
```

**Response**:
```json
[
  {
    "id": 1,
    "short_code": "abc123XY",
    "original_url": "https://example.com/very/long/url",
    "user_id": "your-api-key",
    "created_at": "2026-01-20T10:30:00Z"
  }
]
```

### Delete URL
```http
DELETE /api/urls/{shortCode}
X-API-Key: your-api-key
```

### Get Analytics
```http
GET /api/analytics/{shortCode}
X-API-Key: your-api-key
```

**Response**:
```json
{
  "short_code": "abc123XY",
  "original_url": "https://example.com/very/long/url",
  "total_clicks": 42,
  "recent_clicks": [
    {
      "id": 100,
      "short_code": "abc123XY",
      "clicked_at": "2026-01-20T15:30:00Z",
      "referrer": "https://google.com"
    }
  ],
  "created_at": "2026-01-20 10:30:00"
}
```

## Configuration

Environment variables:

- `PORT` - Server port (default: `8080`)
- `REDIS_ADDR` - Redis address (default: `localhost:6379`)

## Testing

```bash
# Run tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run tests verbosely
go test -v ./...
```

## Example Usage

```bash
# Create a short URL
curl -X POST http://localhost:8080/api/urls \
  -H "X-API-Key: mykey" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://github.com"}'

# Access the short URL (will redirect)
curl -L http://localhost:8080/abc123XY

# List your URLs
curl http://localhost:8080/api/urls \
  -H "X-API-Key: mykey"

# Get analytics
curl http://localhost:8080/api/analytics/abc123XY \
  -H "X-API-Key: mykey"

# Delete a URL
curl -X DELETE http://localhost:8080/api/urls/abc123XY \
  -H "X-API-Key: mykey"
```

## Conversion Target

This application is designed to be converted to **Python with FastAPI**.

### Key Conversion Points:

1. **Chi router → FastAPI**
   - HTTP handlers → FastAPI path operations
   - Middleware → FastAPI dependencies/middleware

2. **Go structs → Pydantic models**
   - Type-safe request/response models
   - Automatic validation

3. **Go interfaces → Python Protocols**
   - Cache interface → ABC or Protocol
   - Store interface → ABC or Protocol

4. **Error handling**
   - Go error returns → Python exceptions
   - Custom error types

5. **Concurrency**
   - Go goroutines → Python async/await
   - Redis operations → async redis

## Database Schema

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    user_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT NOT NULL,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referrer TEXT,
    FOREIGN KEY (short_code) REFERENCES urls(short_code)
);
```

## License

This is a workshop example application.
