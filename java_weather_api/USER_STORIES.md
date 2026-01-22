# Java Weather API - User Stories & Task Distribution

**Team:** 2 Developers  
**Sprint Duration:** ~4-6 weeks (56 items)  
**Strategy:** Parallel development with minimal dependencies  
**Start Date:** January 23, 2026

---

## 👥 Team Assignment Strategy

| Developer | Focus Area | Stories | Est. Hours |
|-----------|-----------|---------|-----------|
| **Developer 1 (Backend/Services)** | Services, Clients, Business Logic | 28 | 70-80 |
| **Developer 2 (API/Database)** | Controllers, Database, Cache, Testing | 28 | 70-80 |

---

# 🔵 Developer 1: Services & External API Integration (28 Stories)

## US-101: Weather API Client

**Story ID:** US-101  
**Priority:** P0 (Critical)  
**Story Points:** 5  
**Assigned To:** Developer 1  

**Description:**  
Create WebClient-based HTTP client for WeatherAPI.com integration with error handling and retry logic.

**Acceptance Criteria:**
- [ ] Create `WeatherApiClient` class using Spring WebClient
- [ ] Implement `getWeather(String location, String unit)` for current weather
- [ ] Implement `getForecast(String location, int days, String unit)` for forecast data
- [ ] Add retry logic with exponential backoff (max 3 retries)
- [ ] Map WeatherAPI.com JSON responses to DTOs
- [ ] Handle API rate limiting (429) and errors gracefully
- [ ] Unit tests with WireMock (80%+ coverage)
- [ ] API timeout configuration (30 seconds default)

**Dependencies:**
- Spring WebFlux/WebClient
- Jackson for JSON mapping
- WireMock for testing
- ApiProperties configuration

**Effort:** 5 hours

---

## US-102: OpenWeather Client

**Story ID:** US-102  
**Priority:** P0 (Critical)  
**Story Points:** 5  
**Assigned To:** Developer 1  

**Description:**  
Create WebClient-based HTTP client for OpenWeatherMap API with similar structure to WeatherAPI client.

**Acceptance Criteria:**
- [ ] Create `OpenWeatherClient` class using Spring WebClient
- [ ] Implement `getWeather(String location, String unit)` for current weather
- [ ] Implement `getForecast(String location, int days, String unit)` for forecast data
- [ ] Add retry logic with exponential backoff (max 3 retries)
- [ ] Map OpenWeatherMap JSON responses to DTOs
- [ ] Handle API rate limiting and errors gracefully
- [ ] Unit tests with WireMock (80%+ coverage)
- [ ] API timeout configuration (30 seconds default)

**Dependencies:**
- Spring WebFlux/WebClient
- Jackson for JSON mapping
- WireMock for testing
- ApiProperties configuration

**Effort:** 5 hours

---

## US-103: Client Factory & Strategy

**Story ID:** US-103  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Create factory pattern for managing multiple weather clients and strategy for client selection.

**Acceptance Criteria:**
- [ ] Create `WeatherClientFactory` with factory pattern
- [ ] Support switching between clients via configuration
- [ ] Implement client selection strategy (all, first available, fallback)
- [ ] Handle client initialization and cleanup
- [ ] Unit tests for factory creation (80%+ coverage)
- [ ] Support multiple client instances

**Dependencies:**
- US-101 (WeatherApiClient)
- US-102 (OpenWeatherClient)
- Spring Boot ConfigurationProperties

**Effort:** 3 hours

---

## US-104: API Configuration Properties

**Story ID:** US-104  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 1  

**Description:**  
Create configuration properties class for externalizing API keys and endpoints.

**Acceptance Criteria:**
- [ ] Create `ApiProperties` class with @ConfigurationProperties
- [ ] Load API keys from `application.yml`
- [ ] Support different endpoints per environment
- [ ] Validate API key presence at startup
- [ ] Add configuration documentation
- [ ] Support API endpoint overrides

**Dependencies:**
- Spring Boot ConfigurationProperties

**Effort:** 2 hours

---

## US-105: Exception Handling

**Story ID:** US-105  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Create custom exception hierarchy and global exception handler for API errors.

**Acceptance Criteria:**
- [ ] Create custom exceptions: `ApiException`, `RateLimitException`, `LocationNotFoundException`
- [ ] Create `GlobalExceptionHandler` with `@RestControllerAdvice`
- [ ] Map exceptions to HTTP status codes (429, 404, 500, etc.)
- [ ] Return consistent error response format
- [ ] Log errors appropriately
- [ ] Unit tests for all exception scenarios (80%+ coverage)

**Dependencies:**
- Spring MVC

**Effort:** 3 hours

---

## US-106: Weather Domain Models

**Story ID:** US-106  
**Priority:** P0 (Critical)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Create domain model classes for weather data (WeatherData, AggregatedWeather, ForecastData).

**Acceptance Criteria:**
- [ ] Create `WeatherData` class with fields: location, temperature, humidity, description, windSpeed, timestamp, source
- [ ] Create `AggregatedWeather` class with aggregated data
- [ ] Create `ForecastData` class with daily forecast items
- [ ] Create `ForecastItem` class for individual forecast entries
- [ ] Add conversion methods to/from DTOs
- [ ] Add validation annotations (NotNull, NotBlank, Positive)
- [ ] Use Lombok annotations for boilerplate
- [ ] Unit tests (100% coverage)

**Dependencies:**
- Jakarta Validation
- Lombok

**Effort:** 3 hours

---

## US-107: Weather Aggregation Service

**Story ID:** US-107  
**Priority:** P0 (Critical)  
**Story Points:** 8  
**Assigned To:** Developer 1  

**Description:**  
Implement service to aggregate weather data from multiple sources with caching integration.

**Acceptance Criteria:**
- [ ] Create `WeatherAggregator` service class
- [ ] Implement `getAggregatedWeather(String location, String unit)` - calls multiple clients, averages data
- [ ] Implement `getForecast(String location, int days, String unit)` - returns forecast from first available source
- [ ] Add consensus logic for weather description (most common character)
- [ ] Integrate with CacheService (interface-based)
- [ ] Handle partial failures (one client down, continue with others)
- [ ] Support parallel API calls with CompletableFuture
- [ ] Log aggregation metrics
- [ ] Unit tests with mocked clients (80%+ coverage)

**Dependencies:**
- US-101 (WeatherApiClient)
- US-102 (OpenWeatherClient)
- US-106 (WeatherData models)
- CacheService interface (from Dev 2)

**Effort:** 8 hours

---

## US-108: Weather Comparison Service

**Story ID:** US-108  
**Priority:** P2 (Medium)  
**Story Points:** 4  
**Assigned To:** Developer 1  

**Description:**  
Implement service to compare weather data between multiple locations.

**Acceptance Criteria:**
- [ ] Create `WeatherComparison` domain model
- [ ] Implement comparison logic (hottest, coldest, most humid, etc.)
- [ ] Support 2-10 locations comparison
- [ ] Return sorted results
- [ ] Add filtering capabilities (temperature range, humidity range)
- [ ] Validate location list (non-empty, unique)
- [ ] Unit tests (80%+ coverage)

**Dependencies:**
- US-107 (WeatherAggregator)

**Effort:** 4 hours

---

## US-109: Temperature Conversion Utility

**Story ID:** US-109  
**Priority:** P2 (Medium)  
**Story Points:** 1  
**Assigned To:** Developer 1  

**Description:**  
Create utility for converting temperature between Celsius and Fahrenheit.

**Acceptance Criteria:**
- [ ] Create `TemperatureConverter` utility class
- [ ] Implement `celsiusToFahrenheit(double celsius)` method
- [ ] Implement `fahrenheitToCelsius(double fahrenheit)` method
- [ ] Add precision handling (2 decimal places)
- [ ] Support BigDecimal for precision
- [ ] Unit tests (100% coverage)

**Dependencies:**
- None

**Effort:** 1 hour

---

## US-110: Retry Logic & Circuit Breaker

**Story ID:** US-110  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Implement retry logic with exponential backoff for API calls.

**Acceptance Criteria:**
- [ ] Create `RetryConfig` class with retry template
- [ ] Configure exponential backoff strategy (1s, 2s, 4s)
- [ ] Support configurable max retries (default 3)
- [ ] Add jitter to prevent thundering herd
- [ ] Log retry attempts
- [ ] Support retry exception filters
- [ ] Unit tests (80%+ coverage)

**Dependencies:**
- Spring Retry or custom implementation

**Effort:** 3 hours

---

## US-111: Response Parsing & Mapping

**Story ID:** US-111  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Implement JSON response parsing and conversion to domain models.

**Acceptance Criteria:**
- [ ] Create response mapping for WeatherAPI.com
- [ ] Create response mapping for OpenWeatherMap
- [ ] Handle nested JSON structures
- [ ] Handle missing/null fields gracefully
- [ ] Add error logging for parse failures
- [ ] Support custom Jackson deserialization
- [ ] Unit tests for all mapping scenarios (85%+ coverage)

**Dependencies:**
- Jackson
- WeatherData models (US-106)
- US-101, US-102 (response DTOs)

**Effort:** 3 hours

---

## US-112: Rate Limiting Handling

**Story ID:** US-112  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 1  

**Description:**  
Implement handling for API rate limits with appropriate responses.

**Acceptance Criteria:**
- [ ] Detect 429 (Too Many Requests) responses
- [ ] Implement backoff strategy for rate limits
- [ ] Return `RateLimitException` with retry-after header
- [ ] Log rate limit incidents
- [ ] Support rate limit quotas configuration
- [ ] Unit tests (80%+ coverage)

**Dependencies:**
- US-105 (RateLimitException)

**Effort:** 2 hours

---

## US-113: API Client Unit Tests

**Story ID:** US-113  
**Priority:** P1 (High)  
**Story Points:** 4  
**Assigned To:** Developer 1  

**Description:**  
Create unit tests for HTTP clients using WireMock for mocking.

**Acceptance Criteria:**
- [ ] Mock WeatherAPI.com endpoints with WireMock
- [ ] Mock OpenWeatherMap endpoints with WireMock
- [ ] Test successful weather retrieval
- [ ] Test error scenarios (404, 500, timeout)
- [ ] Test rate limiting (429)
- [ ] Test network timeout handling
- [ ] Achieve 85%+ coverage for client classes
- [ ] Test concurrent request handling

**Dependencies:**
- WireMock
- JUnit 5
- US-101, US-102

**Effort:** 4 hours

---

## US-114: Service Layer Integration Tests

**Story ID:** US-114  
**Priority:** P1 (High)  
**Story Points:** 5  
**Assigned To:** Developer 1  

**Description:**  
Create integration tests for aggregation service with mocked APIs.

**Acceptance Criteria:**
- [ ] Setup WireMock servers for both APIs
- [ ] Test aggregation with single API response
- [ ] Test aggregation with multiple API responses
- [ ] Test partial failure scenarios
- [ ] Test consensus description calculation
- [ ] Test temperature averaging logic
- [ ] Achieve 80%+ coverage for service layer
- [ ] Test timeout and retry scenarios

**Dependencies:**
- US-107 (WeatherAggregator)
- WireMock
- JUnit 5

**Effort:** 5 hours

---

## US-115: Service Documentation

**Story ID:** US-115  
**Priority:** P2 (Medium)  
**Story Points:** 2  
**Assigned To:** Developer 1  

**Description:**  
Add Springdoc-OpenAPI annotations to service and client classes for auto-documentation.

**Acceptance Criteria:**
- [ ] Add `@Operation` annotations to service methods
- [ ] Add `@Parameter` annotations for method parameters
- [ ] Document request/response schemas
- [ ] Add examples to documentation
- [ ] Document possible exceptions
- [ ] Verify Swagger UI shows service layer info
- [ ] Create developer API reference

**Dependencies:**
- Springdoc-openapi

**Effort:** 2 hours

---

## US-116: Client Response DTOs (WeatherAPI)

**Story ID:** US-116  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 1  

**Description:**  
Create DTOs for WeatherAPI.com response mapping.

**Acceptance Criteria:**
- [ ] Create WeatherApiCurrentResponse DTO
- [ ] Create WeatherApiForecastResponse DTO
- [ ] Add Jackson annotations for JSON mapping
- [ ] Handle nested objects and arrays
- [ ] Add validation annotations
- [ ] Unit tests for DTO creation (80%+ coverage)

**Dependencies:**
- Jackson

**Effort:** 2 hours

---

## US-117: Client Response DTOs (OpenWeather)

**Story ID:** US-117  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 1  

**Description:**  
Create DTOs for OpenWeatherMap response mapping.

**Acceptance Criteria:**
- [ ] Create OpenWeatherCurrentResponse DTO
- [ ] Create OpenWeatherForecastResponse DTO
- [ ] Add Jackson annotations for JSON mapping
- [ ] Handle nested objects and arrays
- [ ] Add validation annotations
- [ ] Unit tests for DTO creation (80%+ coverage)

**Dependencies:**
- Jackson

**Effort:** 2 hours

---

## US-118: Graceful Degradation

**Story ID:** US-118  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Implement graceful degradation when some APIs fail.

**Acceptance Criteria:**
- [ ] Continue aggregation if one API fails
- [ ] Return partial results with available data
- [ ] Log API failure events
- [ ] Notify client about partial data
- [ ] Support fallback to single API
- [ ] Unit tests (80%+ coverage)

**Dependencies:**
- US-107 (WeatherAggregator)

**Effort:** 3 hours

---

## US-119: Concurrent API Calls

**Story ID:** US-119  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 1  

**Description:**  
Implement concurrent API calls using CompletableFuture for performance.

**Acceptance Criteria:**
- [ ] Use CompletableFuture for parallel API calls
- [ ] Implement timeout handling (30 seconds total)
- [ ] Handle individual call timeouts gracefully
- [ ] Log concurrent call metrics
- [ ] Unit tests with latency verification
- [ ] Performance tests showing latency improvement

**Dependencies:**
- US-101, US-102 (API clients)

**Effort:** 3 hours

---

## US-120: Logging & Observability (Services)

**Story ID:** US-120  
**Priority:** P2 (Medium)  
**Story Points:** 2  
**Assigned To:** Developer 1  

**Description:**  
Add comprehensive logging and metrics for services.

**Acceptance Criteria:**
- [ ] Add SLF4J logging to all service methods
- [ ] Log API call start/end with latency
- [ ] Log aggregation metrics (sources used, consensus reached)
- [ ] Log error events with context
- [ ] Support different log levels (DEBUG, INFO, WARN, ERROR)
- [ ] Create structured logging with MDC

**Dependencies:**
- SLF4J/Logback

**Effort:** 2 hours

---

**Developer 1 Summary:** 20 stories, ~65-75 hours

---

# 🟣 Developer 2: Controllers, Database & Cache (28 Stories)

## US-201: PostgreSQL Schema (Flyway V1)

**Story ID:** US-201  
**Priority:** P0 (Critical)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create initial PostgreSQL schema with Flyway migrations for favorites table.

**Acceptance Criteria:**
- [ ] Create `V1__Initial_schema.sql` for favorites table
  - Columns: id (PK BIGSERIAL), location (VARCHAR 255 UNIQUE), added_at (TIMESTAMP), updated_at (TIMESTAMP)
  - Default timestamps with CURRENT_TIMESTAMP
  - NOT NULL constraints on required columns
- [ ] Create audit trigger for updated_at column
- [ ] Add comments for schema documentation
- [ ] Test migration rollback
- [ ] Verify schema in dev/test environments

**Dependencies:**
- Flyway configuration in pom.xml

**Effort:** 3 hours

---

## US-202: Database Indices (Flyway V2)

**Story ID:** US-202  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create Flyway migration for performance optimization with indices.

**Acceptance Criteria:**
- [ ] Create `V2__Add_indexes.sql` with:
  - Index on location (for lookups)
  - Index on added_at (for sorting)
- [ ] Document index rationale
- [ ] Test index creation in dev environment
- [ ] Verify query plans with indices

**Dependencies:**
- US-201 (V1 schema)

**Effort:** 2 hours

---

## US-203: Redis Configuration

**Story ID:** US-203  
**Priority:** P0 (Critical)  
**Story Points:** 4  
**Assigned To:** Developer 2  

**Description:**  
Configure Spring Data Redis for caching with connection pooling.

**Acceptance Criteria:**
- [ ] Create `RedisConfig` class with Spring Data Redis
- [ ] Configure connection pool (HikariCP pattern)
- [ ] Setup JSON serialization with Jackson
- [ ] Configure cache names and TTL
- [ ] Add connection timeout settings
- [ ] Test Redis connection in dev/test
- [ ] Support multiple Redis profiles (dev, test, prod)

**Dependencies:**
- spring-boot-starter-data-redis
- Jedis or Lettuce client
- Jackson

**Effort:** 4 hours

---

## US-204: Cache Service Interface

**Story ID:** US-204  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create CacheService abstraction for flexible cache implementation.

**Acceptance Criteria:**
- [ ] Create `CacheService` interface with methods:
  - `get(key): T`
  - `set(key, value, ttl)`
  - `delete(key)`
  - `clear()`
  - `exists(key)`
- [ ] Add TTL support (milliseconds)
- [ ] Support generic types
- [ ] Document cache contracts

**Dependencies:**
- None (interface only)

**Effort:** 2 hours

---

## US-205: Redis Cache Service Implementation

**Story ID:** US-205  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Implement CacheService with Redis backend.

**Acceptance Criteria:**
- [ ] Implement `RedisCacheService` extending CacheService
- [ ] Implement `get()` with deserialization
- [ ] Implement `set()` with JSON serialization and TTL
- [ ] Implement `delete()` and `clear()`
- [ ] Handle serialization errors gracefully
- [ ] Add metrics for cache hits/misses
- [ ] Unit tests with TestContainers Redis (80%+ coverage)

**Dependencies:**
- US-203 (RedisConfig)
- US-204 (CacheService interface)
- TestContainers Redis

**Effort:** 3 hours

---

## US-206: Cache Annotations Setup

**Story ID:** US-206  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Setup Spring Cache annotations for declarative caching.

**Acceptance Criteria:**
- [ ] Enable `@EnableCaching` in Spring Boot
- [ ] Configure cache manager for Redis
- [ ] Setup default cache names
- [ ] Configure cache key generation strategy
- [ ] Document @Cacheable, @CacheEvict usage
- [ ] Setup cache statistics collection

**Dependencies:**
- Spring Cache abstraction

**Effort:** 2 hours

---

## US-207: Favorites Entity

**Story ID:** US-207  
**Priority:** P0 (Critical)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create JPA entity for favorites with proper mapping.

**Acceptance Criteria:**
- [ ] Create `FavoritesEntity` with JPA annotations
- [ ] Map to favorites table
- [ ] Add fields: id, location, addedAt, updatedAt
- [ ] Add validation annotations (NotBlank, Size, etc.)
- [ ] Add Lombok annotations (@Data, @NoArgsConstructor, @AllArgsConstructor)
- [ ] Add entity lifecycle callbacks (@PrePersist, @PreUpdate)
- [ ] Entity tests (100% coverage)

**Dependencies:**
- Spring Data JPA
- Lombok
- US-201 (Database schema)

**Effort:** 2 hours

---

## US-208: Favorites Repository

**Story ID:** US-208  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create Spring Data JPA repository for favorites.

**Acceptance Criteria:**
- [ ] Create `FavoritesRepository` extending JpaRepository
- [ ] Add custom query methods:
  - `findByLocation(String location)`
  - `existsByLocation(String location)`
  - `findAllByOrderByAddedAtDesc()`
- [ ] Add pagination support via Pageable
- [ ] Add sorting support
- [ ] Repository tests (80%+ coverage)

**Dependencies:**
- US-207 (FavoritesEntity)
- Spring Data JPA

**Effort:** 2 hours

---

## US-209: Weather DTOs

**Story ID:** US-209  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create DTOs for weather request/response.

**Acceptance Criteria:**
- [ ] Create `WeatherDto` for current weather response
- [ ] Create `AggregatedWeatherDto` for aggregated response
- [ ] Create `ForecastDto` for forecast response
- [ ] Create `ForecastItemDto` for individual forecast items
- [ ] Add validation annotations
- [ ] Add Jackson annotations for JSON mapping
- [ ] Add examples for documentation
- [ ] DTO tests (80%+ coverage)

**Dependencies:**
- Jakarta Validation
- Jackson

**Effort:** 3 hours

---

## US-210: Favorites DTOs & Mapper

**Story ID:** US-210  
**Priority:** P1 (High)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create DTOs and mapper for favorites.

**Acceptance Criteria:**
- [ ] Create `FavoritesDto` for request/response
- [ ] Create `FavoritesMapper` interface/implementation
- [ ] Add validation annotations
- [ ] Add examples for documentation
- [ ] Support bidirectional mapping (entity ↔ DTO)
- [ ] Mapper tests (80%+ coverage)

**Dependencies:**
- US-207 (FavoritesEntity)
- MapStruct or manual mapper

**Effort:** 2 hours

---

## US-211: Favorites Service

**Story ID:** US-211  
**Priority:** P1 (High)  
**Story Points:** 4  
**Assigned To:** Developer 2  

**Description:**  
Implement business logic service for favorites management.

**Acceptance Criteria:**
- [ ] Create `FavoritesService` interface
- [ ] Implement `addFavorite(String location)` with duplicate check
- [ ] Implement `removeFavorite(String location)`
- [ ] Implement `getAllFavorites(Pageable)` with pagination
- [ ] Implement `isFavorite(String location)`
- [ ] Handle business logic errors (duplicates, not found)
- [ ] Add transaction management (@Transactional)
- [ ] Service tests with mocked repository (80%+ coverage)

**Dependencies:**
- US-208 (FavoritesRepository)
- US-207 (FavoritesEntity)

**Effort:** 4 hours

---

## US-212: Favorites Controller

**Story ID:** US-212  
**Priority:** P0 (Critical)  
**Story Points:** 4  
**Assigned To:** Developer 2  

**Description:**  
Create REST controller for favorites management.

**Acceptance Criteria:**
- [ ] `GET /api/favorites` - list all favorites with pagination
- [ ] `POST /api/favorites/{location}` - add favorite
- [ ] `DELETE /api/favorites/{location}` - remove favorite
- [ ] `GET /api/favorites/{location}` - check if favorite
- [ ] Proper HTTP status codes (200, 201, 204, 404, 409)
- [ ] Input validation and sanitization
- [ ] API documentation with @Operation, @Parameter
- [ ] Error response handling
- [ ] Controller tests (80%+ coverage)

**Dependencies:**
- US-211 (FavoritesService)
- US-210 (FavoritesDto)

**Effort:** 4 hours

---

## US-213: Weather Controller

**Story ID:** US-213  
**Priority:** P0 (Critical)  
**Story Points:** 5  
**Assigned To:** Developer 2  

**Description:**  
Create REST controller for weather endpoints.

**Acceptance Criteria:**
- [ ] `GET /api/weather/current/{location}?unit=metric|imperial` - current weather
- [ ] `GET /api/weather/forecast/{location}?days=1-7&unit=metric|imperial` - forecast
- [ ] `POST /api/weather/compare` - compare multiple locations
- [ ] Proper HTTP status codes
- [ ] Query parameter validation (unit, days range)
- [ ] Response caching headers (Cache-Control)
- [ ] API documentation with @Operation, @Parameter
- [ ] Error handling and validation
- [ ] Controller tests (80%+ coverage)

**Dependencies:**
- WeatherAggregator (from Dev 1)
- WeatherComparison (from Dev 1)
- US-209 (WeatherDto)
- US-109 (TemperatureConverter)

**Effort:** 5 hours

---

## US-214: Application Configuration Files

**Story ID:** US-214  
**Priority:** P0 (Critical)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create application.yml configuration files for dev, test, prod environments.

**Acceptance Criteria:**
- [ ] Create `application.yml` (shared config)
- [ ] Create `application-dev.yml` (PostgreSQL dev config)
- [ ] Create `application-test.yml` (TestContainers config)
- [ ] Create `application-prod.yml` (production template)
- [ ] Configure database connection pool
- [ ] Configure Redis settings
- [ ] Configure logging levels
- [ ] Document all configuration properties

**Effort:** 3 hours

---

## US-215: Health Check Endpoints

**Story ID:** US-215  
**Priority:** P2 (Medium)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create health check and application info endpoints.

**Acceptance Criteria:**
- [ ] Enable `/actuator/health` endpoint
- [ ] Create custom health indicators for Database
- [ ] Create custom health indicators for Redis
- [ ] Configure health endpoint in application.yml
- [ ] Return appropriate status (UP, DOWN, DEGRADED)
- [ ] Unit tests for health indicators

**Dependencies:**
- spring-boot-starter-actuator

**Effort:** 2 hours

---

## US-216: Springdoc-OpenAPI Configuration

**Story ID:** US-216  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Configure Springdoc-OpenAPI for automatic Swagger documentation.

**Acceptance Criteria:**
- [ ] Create `OpenApiConfig` class
- [ ] Configure OpenAPI info (title, version, description)
- [ ] Configure server information
- [ ] Add security schemes if needed
- [ ] Generate Swagger UI at `/swagger-ui.html`
- [ ] Generate OpenAPI JSON at `/v3/api-docs`
- [ ] Add @Operation, @Parameter annotations to controllers
- [ ] Test Swagger UI generation

**Dependencies:**
- springdoc-openapi-starter-webmvc-ui

**Effort:** 3 hours

---

## US-217: Repository Integration Tests

**Story ID:** US-217  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create integration tests for database layer with TestContainers.

**Acceptance Criteria:**
- [ ] Setup TestContainers PostgreSQL
- [ ] Test FavoritesRepository CRUD operations
- [ ] Test Flyway migration execution
- [ ] Test unique constraint on location
- [ ] Test ordering and pagination
- [ ] 80%+ repository test coverage
- [ ] Test transaction rollback scenarios

**Dependencies:**
- TestContainers PostgreSQL
- US-208 (FavoritesRepository)

**Effort:** 3 hours

---

## US-218: Cache Integration Tests

**Story ID:** US-218  
**Priority:** P1 (High)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create integration tests for Redis caching layer.

**Acceptance Criteria:**
- [ ] Setup TestContainers Redis
- [ ] Test cache hit scenarios
- [ ] Test cache miss scenarios
- [ ] Test TTL expiration
- [ ] Test cache invalidation
- [ ] Test serialization/deserialization
- [ ] 80%+ cache test coverage

**Dependencies:**
- TestContainers Redis
- US-205 (RedisCacheService)

**Effort:** 3 hours

---

## US-219: Controller Unit Tests

**Story ID:** US-219  
**Priority:** P1 (High)  
**Story Points:** 4  
**Assigned To:** Developer 2  

**Description:**  
Create unit tests for REST controllers.

**Acceptance Criteria:**
- [ ] Test successful requests
- [ ] Test error scenarios (400, 404, 409, 500)
- [ ] Test parameter validation
- [ ] Test response format
- [ ] Test HTTP status codes
- [ ] Mock service dependencies
- [ ] 80%+ controller test coverage

**Dependencies:**
- Spring Test
- Mockito
- US-212, US-213

**Effort:** 4 hours

---

## US-220: API Integration Tests

**Story ID:** US-220  
**Priority:** P1 (High)  
**Story Points:** 5  
**Assigned To:** Developer 2  

**Description:**  
Create end-to-end API integration tests with full stack.

**Acceptance Criteria:**
- [ ] Setup @SpringBootTest with TestContainers
- [ ] Test full API flow (request → service → DB → response)
- [ ] Test error scenarios with real database
- [ ] Test concurrent requests
- [ ] Test favorites workflow (add → list → delete)
- [ ] Test weather aggregation with mocked APIs
- [ ] 75%+ integration test coverage

**Dependencies:**
- Spring Boot Test
- TestContainers PostgreSQL + Redis
- WireMock for API mocking

**Effort:** 5 hours

---

## US-221: Logging Configuration

**Story ID:** US-221  
**Priority:** P2 (Medium)  
**Story Points:** 1  
**Assigned To:** Developer 2  

**Description:**  
Configure SLF4J and Logback for structured logging.

**Acceptance Criteria:**
- [ ] Create `logback-spring.xml` configuration
- [ ] Configure log levels per package
- [ ] Setup structured logging with MDC
- [ ] Configure file appenders
- [ ] Configure console appender with colors
- [ ] Setup log rotation policy

**Dependencies:**
- Logback

**Effort:** 1 hour

---

## US-222: Docker Setup

**Story ID:** US-222  
**Priority:** P2 (Medium)  
**Story Points:** 2  
**Assigned To:** Developer 2  

**Description:**  
Create Dockerfile and Docker Compose for containerization.

**Acceptance Criteria:**
- [ ] Create multi-stage Dockerfile
- [ ] Optimize image size
- [ ] Create docker-compose.yml with PostgreSQL and Redis
- [ ] Setup volume mounts for persistence
- [ ] Configure environment variables
- [ ] Test Docker build and run
- [ ] Create .dockerignore file

**Dependencies:**
- Docker

**Effort:** 2 hours

---

## US-223: Documentation & README

**Story ID:** US-223  
**Priority:** P2 (Medium)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create comprehensive README and developer guide.

**Acceptance Criteria:**
- [ ] Create main README.md with project overview
- [ ] Add setup instructions (local, Docker)
- [ ] Document API endpoints with examples
- [ ] Add configuration guide
- [ ] Add deployment instructions
- [ ] Add troubleshooting guide
- [ ] Create CONTRIBUTING.md for developers

**Effort:** 3 hours

---

## US-224: Performance Testing

**Story ID:** US-224  
**Priority:** P2 (Medium)  
**Story Points:** 3  
**Assigned To:** Developer 2  

**Description:**  
Create performance tests for critical paths.

**Acceptance Criteria:**
- [ ] Test cache hit latency (should be <10ms)
- [ ] Test aggregation latency (should be <1s)
- [ ] Test database query performance
- [ ] Load test with multiple concurrent requests
- [ ] Identify and fix performance bottlenecks

**Effort:** 3 hours

---

**Developer 2 Summary:** 24 stories, ~70-80 hours

---

## 📅 Timeline Estimate

| Week | Developer 1 | Developer 2 | Milestone |
|------|-------------|-----------|-----------|
| 1 | US-101-105, US-106 | US-201-207 | Project setup, clients, entities |
| 2 | US-107-112 | US-208-213 | Aggregation service, controllers |
| 3 | US-113-120 | US-214-216 | Testing, config, documentation |
| 4-5 | Remaining | Remaining | Integration tests, refinement |
| 6 | Documentation | Docker/Deploy | Final review, deployment |

---

## 🔄 Dependency Management

**No blockers between developers - can work in parallel:**
- Dev 1: Focus on service layer (US-101 onwards)
- Dev 2: Focus on API layer (US-201 onwards)
- Integration points (caching, DTOs) have clear interfaces

**Key integration points:**
- CacheService interface (US-204) → Used by Dev 1 in US-107
- WeatherDto (US-209) → Used by Dev 2 in US-213
- Temperature converter (US-109) → Used by Dev 2 in US-213

---

## ✅ Definition of Done

For each story:
- [ ] Code implemented and committed
- [ ] Unit tests created (80%+ coverage)
- [ ] Code review approved
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] No new warnings/errors
- [ ] Performance acceptable

---

**Sprint Start:** January 23, 2026  
**Estimated Sprint End:** February-March 2026  
**Team Velocity:** ~15-20 points/week
