# Implementation Plan - Convert Framework Workshop

## Project Overview

This workshop teaches cross-language code conversion using GitHub Copilot. Participants will select applications written in Go or Python and convert them to the opposite language, learning idiomatic patterns, dependency mapping, and migration strategies.

## Source Applications (2 per language, 4 total)

### Go Applications

#### 1. URL Shortener API (`go/url-shortener`)
**Description**: RESTful API for shortening URLs with analytics tracking  
**Lines of Code**: ~600  
**Tech Stack**: Chi router, Redis cache, SQLite database  
**Conversion Target**: Python (FastAPI)

**Features**:
- Shorten long URLs to unique short codes
- Redirect from short URL to original URL
- Track click analytics (count, timestamps, referrers)
- List all shortened URLs for a user
- Delete shortened URLs
- In-memory cache with Redis for fast lookups

**Architecture**:
```
cmd/server/
  main.go                 # Entry point, server setup
internal/
  handler/
    url_handler.go        # HTTP handlers (create, redirect, list, delete)
    analytics_handler.go  # Analytics endpoints
  service/
    url_service.go        # Business logic for URL operations
    analytics_service.go  # Analytics aggregation logic
  storage/
    redis_cache.go        # Redis cache implementation
    sqlite_store.go       # SQLite database operations
  models/
    url.go                # URL model struct
    analytics.go          # Analytics model struct
  middleware/
    auth.go               # Simple API key authentication
    logging.go            # Request logging middleware
go.mod
go.sum
```

**Key Functions & Signatures**:

`internal/handler/url_handler.go`:
```go
type URLHandler struct {
    service *service.URLService
}

func NewURLHandler(service *service.URLService) *URLHandler
func (h *URLHandler) CreateShortURL(w http.ResponseWriter, r *http.Request)
func (h *URLHandler) RedirectURL(w http.ResponseWriter, r *http.Request)
func (h *URLHandler) ListURLs(w http.ResponseWriter, r *http.Request)
func (h *URLHandler) DeleteURL(w http.ResponseWriter, r *http.Request)
```

`internal/service/url_service.go`:
```go
type URLService struct {
    cache storage.Cache
    store storage.Store
}

func NewURLService(cache storage.Cache, store storage.Store) *URLService
func (s *URLService) CreateShortURL(originalURL string, userID string) (*models.URL, error)
func (s *URLService) GetOriginalURL(shortCode string) (string, error)
func (s *URLService) ListUserURLs(userID string) ([]*models.URL, error)
func (s *URLService) DeleteURL(shortCode string, userID string) error
func (s *URLService) generateShortCode() string
```

`internal/storage/redis_cache.go`:
```go
type Cache interface {
    Get(key string) (string, error)
    Set(key string, value string, expiration time.Duration) error
    Delete(key string) error
}

type RedisCache struct {
    client *redis.Client
}

func NewRedisCache(addr string) (*RedisCache, error)
```

`internal/storage/sqlite_store.go`:
```go
type Store interface {
    CreateURL(url *models.URL) error
    GetURL(shortCode string) (*models.URL, error)
    GetUserURLs(userID string) ([]*models.URL, error)
    DeleteURL(shortCode string) error
    RecordClick(shortCode string, referrer string) error
}

type SQLiteStore struct {
    db *sql.DB
}

func NewSQLiteStore(dbPath string) (*SQLiteStore, error)
```

**Database Schema**:
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

**API Endpoints**:
- `POST /api/urls` - Create short URL
- `GET /{shortCode}` - Redirect to original URL
- `GET /api/urls` - List user's URLs
- `DELETE /api/urls/{shortCode}` - Delete URL
- `GET /api/analytics/{shortCode}` - Get click analytics

**Tests**:
- Unit tests for service layer (mocked storage)
- Integration tests for handlers (test server)
- Table-driven tests for edge cases

---

#### 2. Blog REST API (`go/blog-api`)
**Description**: RESTful API for a blog platform with posts, comments, and tags  
**Lines of Code**: ~700  
**Tech Stack**: Gin framework, PostgreSQL, JWT authentication  
**Conversion Target**: Python (Django REST Framework)

**Features**:
- User authentication with JWT tokens
- Create, read, update, delete blog posts
- Add comments to posts
- Tag posts with multiple tags
- Filter posts by tags
- Search posts by title/content
- User authorization (only owner can edit/delete)

**Architecture**:
```
cmd/server/
  main.go                 # Entry point, server setup
internal/
  handler/
    auth_handler.go       # Login, register endpoints
    post_handler.go       # Post CRUD operations
    comment_handler.go    # Comment operations
    tag_handler.go        # Tag operations
  service/
    auth_service.go       # Authentication logic, JWT generation
    post_service.go       # Post business logic
    comment_service.go    # Comment business logic
  repository/
    user_repository.go    # User database operations
    post_repository.go    # Post database operations
    comment_repository.go # Comment database operations
  models/
    user.go               # User model
    post.go               # Post model
    comment.go            # Comment model
    tag.go                # Tag model
  middleware/
    auth_middleware.go    # JWT validation middleware
    cors.go               # CORS middleware
  utils/
    jwt.go                # JWT helper functions
    password.go           # Password hashing
go.mod
go.sum
```

**Key Functions & Signatures**:

`internal/handler/post_handler.go`:
```go
type PostHandler struct {
    service *service.PostService
}

func NewPostHandler(service *service.PostService) *PostHandler
func (h *PostHandler) CreatePost(c *gin.Context)
func (h *PostHandler) GetPost(c *gin.Context)
func (h *PostHandler) ListPosts(c *gin.Context)
func (h *PostHandler) UpdatePost(c *gin.Context)
func (h *PostHandler) DeletePost(c *gin.Context)
func (h *PostHandler) SearchPosts(c *gin.Context)
```

`internal/service/post_service.go`:
```go
type PostService struct {
    postRepo    repository.PostRepository
    tagRepo     repository.TagRepository
}

func NewPostService(postRepo repository.PostRepository, tagRepo repository.TagRepository) *PostService
func (s *PostService) CreatePost(post *models.Post, tagNames []string) error
func (s *PostService) GetPostByID(id int64) (*models.Post, error)
func (s *PostService) ListPosts(limit, offset int, tagFilter string) ([]*models.Post, error)
func (s *PostService) UpdatePost(id int64, post *models.Post, userID int64) error
func (s *PostService) DeletePost(id int64, userID int64) error
func (s *PostService) SearchPosts(query string) ([]*models.Post, error)
```

`internal/repository/post_repository.go`:
```go
type PostRepository interface {
    Create(post *models.Post) error
    GetByID(id int64) (*models.Post, error)
    List(limit, offset int) ([]*models.Post, error)
    ListByTag(tagID int64, limit, offset int) ([]*models.Post, error)
    Update(post *models.Post) error
    Delete(id int64) error
    Search(query string) ([]*models.Post, error)
}

type PostgresPostRepository struct {
    db *sql.DB
}

func NewPostRepository(db *sql.DB) *PostgresPostRepository
```

**Database Schema**:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**API Endpoints**:
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/posts` - Create post (authenticated)
- `GET /api/posts` - List posts with pagination
- `GET /api/posts/:id` - Get single post
- `PUT /api/posts/:id` - Update post (owner only)
- `DELETE /api/posts/:id` - Delete post (owner only)
- `GET /api/posts/search` - Search posts
- `POST /api/posts/:id/comments` - Add comment
- `GET /api/tags` - List all tags

**Tests**:
- Unit tests for service layer
- Integration tests for API endpoints
- Authentication/authorization tests
- Database transaction tests

---

### Python Applications

#### 3. Weather CLI Tool (`python/weather-cli`)
**Description**: Command-line tool to fetch and display weather data from multiple sources  
**Lines of Code**: ~500  
**Tech Stack**: Click (CLI framework), Requests, SQLite caching  
**Conversion Target**: Go (Cobra CLI)

**Features**:
- Fetch weather data from multiple APIs (OpenWeatherMap, WeatherAPI)
- Display current weather and forecast
- Support multiple output formats (table, JSON, simple)
- Cache results to reduce API calls
- Store favorite locations
- Compare weather across locations
- Historical data tracking

**Architecture**:
```
weather_cli/
  __init__.py
  cli.py                 # Click CLI commands and groups
  weather/
    __init__.py
    api_client.py        # API client base class
    openweather.py       # OpenWeatherMap implementation
    weatherapi.py        # WeatherAPI implementation
    aggregator.py        # Aggregate data from multiple sources
  storage/
    __init__.py
    cache.py             # SQLite-based caching
    favorites.py         # Favorite locations storage
  formatters/
    __init__.py
    table_formatter.py   # Table output formatter
    json_formatter.py    # JSON output formatter
    simple_formatter.py  # Simple text formatter
  models/
    __init__.py
    weather.py           # Weather data models
  utils/
    __init__.py
    config.py            # Configuration management
    units.py             # Unit conversion (C/F, km/mi)
tests/
  test_api_client.py
  test_cache.py
  test_formatters.py
pyproject.toml
requirements.txt
```

**Key Classes & Functions**:

`weather_cli/cli.py`:
```python
import click
from weather_cli.weather.aggregator import WeatherAggregator

@click.group()
@click.pass_context
def cli(ctx):
    """Weather CLI Tool - Get weather data from multiple sources"""
    pass

@cli.command()
@click.argument('location')
@click.option('--format', type=click.Choice(['table', 'json', 'simple']), default='table')
@click.option('--units', type=click.Choice(['metric', 'imperial']), default='metric')
@click.pass_context
def current(ctx, location: str, format: str, units: str):
    """Get current weather for a location"""
    pass

@cli.command()
@click.argument('location')
@click.option('--days', type=int, default=5)
@click.pass_context
def forecast(ctx, location: str, days: int):
    """Get weather forecast"""
    pass

@cli.command()
@click.argument('location')
def add_favorite(location: str):
    """Add a location to favorites"""
    pass

@cli.command()
def list_favorites():
    """List all favorite locations"""
    pass
```

`weather_cli/weather/api_client.py`:
```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from weather_cli.models.weather import WeatherData

class WeatherAPIClient(ABC):
    """Base class for weather API clients"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    async def get_current_weather(self, location: str) -> WeatherData:
        """Fetch current weather for a location"""
        pass
    
    @abstractmethod
    async def get_forecast(self, location: str, days: int) -> list[WeatherData]:
        """Fetch weather forecast"""
        pass
    
    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to API"""
        pass
```

`weather_cli/weather/openweather.py`:
```python
from weather_cli.weather.api_client import WeatherAPIClient
from weather_cli.models.weather import WeatherData

class OpenWeatherClient(WeatherAPIClient):
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, location: str) -> WeatherData:
        """Implementation for OpenWeatherMap API"""
        pass
    
    async def get_forecast(self, location: str, days: int) -> list[WeatherData]:
        """Implementation for OpenWeatherMap forecast"""
        pass
    
    def _parse_response(self, data: dict) -> WeatherData:
        """Parse API response into WeatherData model"""
        pass
```

`weather_cli/weather/aggregator.py`:
```python
from typing import List
from weather_cli.weather.api_client import WeatherAPIClient
from weather_cli.models.weather import WeatherData, AggregatedWeather
from weather_cli.storage.cache import WeatherCache

class WeatherAggregator:
    """Aggregate weather data from multiple sources"""
    
    def __init__(self, clients: List[WeatherAPIClient], cache: WeatherCache):
        self.clients = clients
        self.cache = cache
    
    async def get_current_weather(self, location: str, use_cache: bool = True) -> AggregatedWeather:
        """Get weather from all sources and aggregate"""
        pass
    
    def _aggregate_data(self, data_list: List[WeatherData]) -> AggregatedWeather:
        """Aggregate data from multiple sources (average, consensus)"""
        pass
```

`weather_cli/storage/cache.py`:
```python
import sqlite3
from datetime import datetime, timedelta
from typing import Optional
from weather_cli.models.weather import WeatherData

class WeatherCache:
    """SQLite-based cache for weather data"""
    
    def __init__(self, db_path: str = "weather_cache.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        pass
    
    def get(self, location: str, max_age: timedelta = timedelta(hours=1)) -> Optional[WeatherData]:
        """Get cached weather data if not expired"""
        pass
    
    def set(self, location: str, data: WeatherData):
        """Cache weather data"""
        pass
    
    def clear_expired(self):
        """Remove expired cache entries"""
        pass
```

`weather_cli/models/weather.py`:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class WeatherData:
    """Weather data model"""
    location: str
    temperature: float  # Celsius
    feels_like: float
    humidity: int  # Percentage
    description: str
    wind_speed: float  # km/h
    timestamp: datetime
    source: str  # API source name
    
    def to_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit"""
        return (self.temperature * 9/5) + 32

@dataclass
class AggregatedWeather:
    """Aggregated weather data from multiple sources"""
    location: str
    avg_temperature: float
    avg_humidity: float
    sources: list[WeatherData]
    consensus_description: str
```

**Database Schema**:
```sql
CREATE TABLE cache (
    location TEXT PRIMARY KEY,
    data TEXT NOT NULL,  -- JSON serialized WeatherData
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT UNIQUE NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    temperature REAL,
    humidity INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**CLI Commands**:
```bash
weather current "Bangkok"
weather current "Bangkok" --format json --units imperial
weather forecast "Tokyo" --days 7
weather add-favorite "New York"
weather list-favorites
weather compare "Bangkok" "Tokyo" "New York"
```

**Tests**:
- Unit tests with mocked API responses
- Cache behavior tests
- Formatter output tests
- CLI command integration tests

---

#### 4. Web Scraper (`python/web-scraper`)
**Description**: Configurable web scraper with data extraction and export capabilities  
**Lines of Code**: ~600  
**Tech Stack**: BeautifulSoup4, Requests, Pandas  
**Conversion Target**: Go (Colly/goquery)

**Features**:
- Scrape websites with configurable selectors
- Extract structured data (text, attributes, links)
- Handle pagination automatically
- Export data to CSV, JSON, Excel
- Rate limiting and retry logic
- Support for JavaScript-rendered sites (optional Selenium)
- Data validation and cleaning

**Architecture**:
```
web_scraper/
  __init__.py
  scraper.py             # Main scraper class
  config/
    __init__.py
    scraper_config.py    # Configuration models
    config_loader.py     # Load configs from YAML
  extractors/
    __init__.py
    base_extractor.py    # Base extractor interface
    css_extractor.py     # CSS selector extraction
    xpath_extractor.py   # XPath extraction
    regex_extractor.py   # Regex pattern extraction
  exporters/
    __init__.py
    csv_exporter.py      # CSV export
    json_exporter.py     # JSON export
    excel_exporter.py    # Excel export
  utils/
    __init__.py
    http_client.py       # HTTP client with retry logic
    rate_limiter.py      # Rate limiting
    validator.py         # Data validation
    cleaner.py           # Data cleaning utilities
  models/
    __init__.py
    scrape_result.py     # Scraped data models
tests/
  test_scraper.py
  test_extractors.py
  test_exporters.py
  fixtures/
    sample.html          # Test HTML files
pyproject.toml
requirements.txt
```

**Key Classes & Functions**:

`web_scraper/scraper.py`:
```python
from typing import List, Dict, Any
from web_scraper.config.scraper_config import ScraperConfig
from web_scraper.utils.http_client import HTTPClient
from web_scraper.extractors.base_extractor import Extractor
from web_scraper.models.scrape_result import ScrapeResult

class WebScraper:
    """Main web scraper class"""
    
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.http_client = HTTPClient(
            rate_limit=config.rate_limit,
            retry_count=config.retry_count
        )
        self.extractors: List[Extractor] = []
    
    def add_extractor(self, extractor: Extractor):
        """Add data extractor"""
        self.extractors.append(extractor)
    
    async def scrape(self, url: str) -> ScrapeResult:
        """Scrape a single page"""
        pass
    
    async def scrape_multiple(self, urls: List[str]) -> List[ScrapeResult]:
        """Scrape multiple pages"""
        pass
    
    async def scrape_with_pagination(self, start_url: str) -> List[ScrapeResult]:
        """Scrape pages with automatic pagination"""
        pass
    
    def _extract_data(self, html: str) -> Dict[str, Any]:
        """Extract data using all configured extractors"""
        pass
    
    def _find_next_page(self, html: str) -> str | None:
        """Find next page URL for pagination"""
        pass
```

`web_scraper/config/scraper_config.py`:
```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ExtractorConfig:
    """Configuration for a single extractor"""
    name: str
    type: str  # 'css', 'xpath', 'regex'
    selector: str
    attribute: Optional[str] = None  # For extracting attributes
    multiple: bool = False  # Extract multiple matches
    
@dataclass
class ScraperConfig:
    """Main scraper configuration"""
    name: str
    base_url: str
    extractors: List[ExtractorConfig]
    pagination_selector: Optional[str] = None
    rate_limit: float = 1.0  # Requests per second
    retry_count: int = 3
    timeout: int = 30
    headers: Dict[str, str] = None
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ScraperConfig':
        """Load configuration from YAML file"""
        pass
```

`web_scraper/extractors/css_extractor.py`:
```python
from bs4 import BeautifulSoup
from web_scraper.extractors.base_extractor import Extractor
from typing import Any, List

class CSSExtractor(Extractor):
    """Extract data using CSS selectors"""
    
    def __init__(self, name: str, selector: str, attribute: str = None, multiple: bool = False):
        self.name = name
        self.selector = selector
        self.attribute = attribute
        self.multiple = multiple
    
    def extract(self, html: str) -> Any:
        """Extract data from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        if self.multiple:
            elements = soup.select(self.selector)
            return self._extract_from_elements(elements)
        else:
            element = soup.select_one(self.selector)
            return self._extract_from_element(element)
    
    def _extract_from_element(self, element) -> Any:
        """Extract data from a single element"""
        if element is None:
            return None
        
        if self.attribute:
            return element.get(self.attribute)
        return element.get_text(strip=True)
    
    def _extract_from_elements(self, elements: List) -> List[Any]:
        """Extract data from multiple elements"""
        return [self._extract_from_element(el) for el in elements]
```

`web_scraper/utils/http_client.py`:
```python
import requests
import time
from typing import Dict, Optional
from web_scraper.utils.rate_limiter import RateLimiter

class HTTPClient:
    """HTTP client with retry logic and rate limiting"""
    
    def __init__(self, rate_limit: float = 1.0, retry_count: int = 3, timeout: int = 30):
        self.rate_limiter = RateLimiter(rate_limit)
        self.retry_count = retry_count
        self.timeout = timeout
        self.session = requests.Session()
    
    async def get(self, url: str, headers: Dict[str, str] = None) -> str:
        """Fetch URL with retry logic"""
        self.rate_limiter.wait_if_needed()
        
        for attempt in range(self.retry_count):
            try:
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == self.retry_count - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
```

`web_scraper/exporters/csv_exporter.py`:
```python
import csv
from typing import List, Dict, Any
from web_scraper.models.scrape_result import ScrapeResult

class CSVExporter:
    """Export scraped data to CSV"""
    
    def export(self, results: List[ScrapeResult], output_path: str):
        """Export results to CSV file"""
        if not results:
            return
        
        # Get all unique keys from results
        all_keys = set()
        for result in results:
            all_keys.update(result.data.keys())
        
        fieldnames = ['url', 'scraped_at'] + sorted(all_keys)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = {
                    'url': result.url,
                    'scraped_at': result.scraped_at.isoformat(),
                    **result.data
                }
                writer.writerow(row)
```

`web_scraper/models/scrape_result.py`:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass
class ScrapeResult:
    """Result of a scraping operation"""
    url: str
    data: Dict[str, Any]
    scraped_at: datetime
    success: bool
    error: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'url': self.url,
            'data': self.data,
            'scraped_at': self.scraped_at.isoformat(),
            'success': self.success,
            'error': self.error
        }
```

**Example Configuration (YAML)**:
```yaml
name: "Product Scraper"
base_url: "https://example.com"
rate_limit: 2.0
retry_count: 3
timeout: 30

headers:
  User-Agent: "Mozilla/5.0 (compatible; WebScraper/1.0)"

extractors:
  - name: "title"
    type: "css"
    selector: "h1.product-title"
    
  - name: "price"
    type: "css"
    selector: "span.price"
    
  - name: "images"
    type: "css"
    selector: "img.product-image"
    attribute: "src"
    multiple: true
    
  - name: "description"
    type: "css"
    selector: "div.description"

pagination_selector: "a.next-page"
```

**Usage Example**:
```python
from web_scraper import WebScraper
from web_scraper.config import ScraperConfig
from web_scraper.exporters import CSVExporter

# Load configuration
config = ScraperConfig.from_yaml("product_scraper.yaml")

# Create scraper
scraper = WebScraper(config)

# Scrape with pagination
results = await scraper.scrape_with_pagination("https://example.com/products")

# Export to CSV
exporter = CSVExporter()
exporter.export(results, "products.csv")
```

**Tests**:
- Unit tests with mock HTML responses
- Extractor accuracy tests
- Rate limiter tests
- Export format validation tests
- Integration tests with real websites (test sites only)

---

## Conversion Paths

### Path 1: URL Shortener (Go → Python)
**Target**: FastAPI with Redis and SQLite  
**Complexity**: Medium  
**Estimated Time**: 2-3 hours

**Key Conversions**:
1. Chi router → FastAPI routing with path operations
2. Go structs → Pydantic models
3. Go interfaces → Python Protocols/ABC
4. SQL database operations → SQLAlchemy or raw SQL with type hints
5. Redis operations → redis-py with async support
6. Middleware → FastAPI dependencies and middleware
7. Go error handling → Python exceptions
8. Table-driven tests → pytest with parametrize

**Dependencies Mapping**:
- Chi → FastAPI
- go-redis → redis-py
- database/sql → sqlite3 or SQLAlchemy
- testify → pytest

**Challenges**:
- Async/await patterns for I/O operations
- Type safety without compile-time checking
- Context management vs dependency injection

---

### Path 2: Blog API (Go → Python)
**Target**: Django REST Framework with PostgreSQL  
**Complexity**: High  
**Estimated Time**: 3-4 hours

**Key Conversions**:
1. Gin framework → Django REST Framework
2. Repository pattern → Django ORM models
3. JWT middleware → Django REST Framework JWT
4. Go structs → Django models and serializers
5. Manual routing → Django URL patterns
6. Custom authentication → Django authentication system
7. SQL queries → Django ORM queries
8. Go testing → Django test framework

**Dependencies Mapping**:
- Gin → Django + DRF
- JWT library → djangorestframework-simplejwt
- pq (PostgreSQL driver) → psycopg2
- testify → Django TestCase

**Challenges**:
- Learning Django conventions
- ORM vs manual SQL
- Django's "batteries included" vs explicit Go approach

---

### Path 3: Weather CLI (Python → Go)
**Target**: Cobra CLI with SQLite  
**Complexity**: Medium  
**Estimated Time**: 2-3 hours

**Key Conversions**:
1. Click framework → Cobra CLI framework
2. Python classes → Go structs with methods
3. Async operations → goroutines
4. Dataclasses → Go structs with JSON tags
5. SQLite with ORM → database/sql with raw queries
6. Exception handling → error returns
7. Pytest → Go testing package

**Dependencies Mapping**:
- Click → Cobra
- Requests → net/http or resty
- BeautifulSoup → goquery (if needed)
- Pytest → testing package

**Challenges**:
- No async/await in Go (use goroutines differently)
- Manual error handling vs exceptions
- No dataclass magic (explicit struct definitions)
- Formatted output without rich Python libraries

---

### Path 4: Web Scraper (Python → Go)
**Target**: Colly framework with goquery  
**Complexity**: High  
**Estimated Time**: 3-4 hours

**Key Conversions**:
1. BeautifulSoup → goquery
2. Python classes → Go structs and interfaces
3. Async operations → concurrent goroutines
4. Pandas export → encoding/csv and JSON
5. YAML config → viper or yaml.v3
6. Rate limiting → time.Ticker or custom implementation
7. Dataclasses → Go structs
8. Pytest → Go table-driven tests

**Dependencies Mapping**:
- BeautifulSoup4 → goquery
- Requests → colly or net/http
- Pandas → encoding/csv + custom logic
- PyYAML → gopkg.in/yaml.v3

**Challenges**:
- No BeautifulSoup equivalent (goquery is jQuery-like)
- Manual CSV/Excel writing vs Pandas
- Rate limiting implementation from scratch
- Type safety requires more boilerplate

---

## Workshop Flow

### Module 1: Setup & Introduction (30 minutes)
1. Clone repository
2. Review source applications
3. Choose conversion path
4. Setup development environment
5. Review Copilot best practices

### Module 2: Core Conversion (Demo - 45 minutes)
**Instructor demonstrates converting one small module**

For URL Shortener (Go → Python) example:
1. Convert models (structs → Pydantic)
2. Convert storage layer (interfaces → ABC)
3. Convert one handler (Chi → FastAPI)
4. Convert tests
5. Discuss Copilot techniques used

### Module 3: Hands-On Conversion (90-120 minutes)
Participants work on their chosen application:

**Checkpoints**:
1. Models converted ✓
2. Storage/repository layer converted ✓
3. Business logic converted ✓
4. API/CLI interface converted ✓
5. Tests passing ✓
6. Documentation updated ✓

**Support**:
- Instructor available for questions
- Reference implementation available (hidden branch)
- Copilot guide for common patterns

### Module 4: Review & Best Practices (30 minutes)
1. Review converted applications
2. Discuss challenges encountered
3. Share Copilot techniques that worked
4. Compare idiomatic patterns
5. Performance considerations

---

## Testing Strategy

### Conversion Validation
Each conversion must pass:

1. **Functionality Tests**
   - All original features work
   - Same input/output behavior
   - Edge cases handled

2. **Code Quality**
   - Idiomatic code in target language
   - Proper error handling
   - Type safety (where applicable)

3. **Test Coverage**
   - Tests converted and passing
   - Coverage similar to original
   - New language-specific tests added

4. **Documentation**
   - README updated
   - API documentation complete
   - Setup instructions clear

---

## Acceptance Criteria

### Per Application Conversion

#### Functional Requirements
- [ ] All endpoints/commands work correctly
- [ ] Database operations successful
- [ ] External API integrations work
- [ ] Authentication/authorization (if applicable)
- [ ] Data validation working
- [ ] Error handling in place

#### Code Quality
- [ ] Follows target language conventions
- [ ] No obvious bugs or anti-patterns
- [ ] Proper dependency management
- [ ] Configuration externalized
- [ ] Logging implemented

#### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Test coverage > 70%
- [ ] Edge cases covered

#### Documentation
- [ ] README.md with setup instructions
- [ ] API documentation (if API)
- [ ] Code comments for complex logic
- [ ] Conversion notes documented

---

## Timeline

### Pre-Workshop (1 week before)
- [ ] Complete all source applications
- [ ] Write comprehensive tests
- [ ] Create reference conversions
- [ ] Test workshop flow
- [ ] Prepare presentation materials

### Workshop Day
- **09:00-09:30**: Setup & Introduction
- **09:30-10:15**: Demo conversion (Module 2)
- **10:15-10:30**: Break
- **10:30-12:30**: Hands-on conversion (Module 3)
- **12:30-13:30**: Lunch
- **13:30-15:30**: Continue conversion (Module 3)
- **15:30-15:45**: Break
- **15:45-16:15**: Review & Best Practices (Module 4)
- **16:15-16:30**: Q&A and Wrap-up

---

## Success Metrics

1. **Completion Rate**: % of participants who complete conversion
2. **Code Quality**: Review of idiomatic patterns used
3. **Copilot Usage**: Effectiveness of AI assistance
4. **Participant Feedback**: Survey scores
5. **Learning Outcomes**: Post-workshop assessment

---

## Next Steps After Workshop

Participants can:
1. Complete remaining conversions
2. Add advanced features
3. Optimize performance
4. Deploy applications
5. Share learnings with team
6. Contribute improvements to workshop materials
