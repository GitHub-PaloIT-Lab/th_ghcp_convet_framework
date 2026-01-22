# Weather API - Java Spring Boot Implementation

เป็นการ migrate จาก Python FastAPI ไปเป็น Java Spring Boot โดยรวมข้อมูลสภาพอากาศจากหลายแหล่ง (WeatherAPI.com, OpenWeatherMap)

## 🎯 Features

- ✅ ข้อมูลสภาพอากาศปัจจุบัน (Current Weather)
- ✅ พยากรณ์อากาศ 1-7 วัน (Weather Forecast)
- ✅ เปรียบเทียบสภาพอากาศหลายเมือง (City Comparison)
- ✅ จัดการเมืองโปรด (Favorites Management)
- ✅ Redis Caching สำหรับ performance
- ✅ PostgreSQL สำหรับเก็บข้อมูล favorites
- ✅ Swagger UI สำหรับ API documentation
- ✅ Docker support

## 🛠️ Tech Stack

- **Java 17**
- **Spring Boot 3.2.1**
- **Spring Data JPA**
- **PostgreSQL 15**
- **Redis 7**
- **Spring WebFlux (WebClient)**
- **Flyway** (Database migrations)
- **Lombok** (Boilerplate reduction)
- **Springdoc OpenAPI** (Swagger UI)

## 📋 Prerequisites

- Java 17 หรือสูงกว่า
- Maven 3.9+
- Docker และ Docker Compose
- API Keys:
  - [WeatherAPI.com](https://www.weatherapi.com/) (ฟรี)
  - [OpenWeatherMap](https://openweathermap.org/api) (ฟรี - optional)

## 🚀 Quick Start

### 1. Clone repository

```bash
git clone <repository-url>
cd java_weather_api
```

### 2. Setup environment

```bash
# Copy environment template
cp .env.example .env

# แก้ไข .env และใส่ API keys
nano .env
```

### 3. Start dependencies (PostgreSQL + Redis)

```bash
docker-compose up -d
```

### 4. Build และ run application

```bash
# Build project
mvn clean install

# Run application
mvn spring-boot:run

# หรือ run with specific profile
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=dev"
```

Application จะรันที่: **http://localhost:8080**

## 📚 API Documentation

เมื่อ application รันอยู่แล้ว สามารถเข้า Swagger UI ได้ที่:

**http://localhost:8080/swagger-ui.html**

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

### Weather Endpoints

#### 1. ข้อมูลสภาพอากาศปัจจุบัน
```bash
curl http://localhost:8080/weather/current/Bangkok
```

Response:
```json
{
  "location": "Bangkok",
  "avg_temperature": 32.5,
  "avg_humidity": 70.0,
  "consensus_description": "Partly cloudy",
  "sources": [
    {
      "source": "WeatherAPI.com",
      "temperature": 32.5,
      "humidity": 70.0,
      "description": "Partly cloudy"
    }
  ],
  "timestamp": "2026-01-22T07:24:41"
}
```

#### 2. พยากรณ์อากาศ
```bash
curl "http://localhost:8080/weather/forecast/Bangkok?days=5"
```

#### 3. เปรียบเทียบสภาพอากาศหลายเมือง
```bash
curl -X POST http://localhost:8080/weather/compare \
  -H "Content-Type: application/json" \
  -d '{"locations": ["Bangkok", "Tokyo", "Singapore"]}'
```

### Favorites Endpoints

#### 1. ดูรายการเมืองโปรดทั้งหมด
```bash
curl http://localhost:8080/favorites
```

#### 2. เพิ่มเมืองโปรด
```bash
curl -X POST http://localhost:8080/favorites/Bangkok
```

#### 3. ดูข้อมูลเมืองโปรด
```bash
curl http://localhost:8080/favorites/Bangkok
```

#### 4. ลบเมืองโปรด
```bash
curl -X DELETE http://localhost:8080/favorites/Bangkok
```

#### 5. ตรวจสอบว่าเป็นเมืองโปรดหรือไม่
```bash
curl http://localhost:8080/favorites/Bangkok/exists
```

## 🧪 Testing

### Run all tests
```bash
mvn test
```

### Run specific test
```bash
mvn test -Dtest=FavoritesServiceTest
```

### Generate coverage report
```bash
mvn jacoco:report
open target/site/jacoco/index.html
```

## 🐳 Docker Deployment

### Build Docker image
```bash
docker build -t weather-api:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

Services จะรันที่:
- **Application**: http://localhost:8080
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Stop services
```bash
docker-compose down
```

### Clean up with volumes
```bash
docker-compose down -v
```

## ⚙️ Configuration

### Application Profiles

- **dev**: Development profile (verbose logging, all actuator endpoints)
- **test**: Testing profile (H2 in-memory database)
- **prod**: Production profile (optimized settings)

### Environment Variables

สามารถ override configuration ผ่าน environment variables:

```bash
# API Keys
WEATHER_API_WEATHERAPIKEY=your-api-key
WEATHER_API_OPENWEATHERAPIKEY=your-api-key

# Database
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/weather_api_db
SPRING_DATASOURCE_USERNAME=weather_user
SPRING_DATASOURCE_PASSWORD=weather_pass

# Redis
SPRING_DATA_REDIS_HOST=localhost
SPRING_DATA_REDIS_PORT=6379

# Application
SPRING_PROFILES_ACTIVE=dev
SERVER_PORT=8080
```

## 📊 Monitoring

### Actuator Endpoints

```bash
# Health check
curl http://localhost:8080/actuator/health

# Application info
curl http://localhost:8080/actuator/info

# Metrics
curl http://localhost:8080/actuator/metrics
```

## 🗂️ Project Structure

```
java_weather_api/
├── src/
│   ├── main/
│   │   ├── java/com/weatherapi/
│   │   │   ├── WeatherApiApplication.java    # Main application
│   │   │   ├── config/                       # Configuration classes
│   │   │   ├── controller/                   # REST controllers
│   │   │   ├── service/                      # Business logic
│   │   │   ├── client/                       # External API clients
│   │   │   ├── entity/                       # JPA entities
│   │   │   ├── dto/                          # Data Transfer Objects
│   │   │   ├── exception/                    # Exception handling
│   │   │   ├── repository/                   # Data access layer
│   │   │   └── util/                         # Utilities
│   │   └── resources/
│   │       ├── application.yml               # Base configuration
│   │       ├── application-dev.yml           # Dev config
│   │       ├── application-prod.yml          # Prod config
│   │       └── db/migration/                 # Flyway migrations
│   └── test/
│       └── java/com/weatherapi/              # Test classes
├── pom.xml                                   # Maven configuration
├── Dockerfile                                # Docker build
├── docker-compose.yml                        # Local dev environment
└── .env.example                              # Environment template
```

## 🔧 Development

### Code Quality

```bash
# Run Checkstyle
mvn checkstyle:check

# Run SpotBugs
mvn spotbugs:check

# Run all quality checks
mvn verify
```

### Database Migrations

Flyway migrations อยู่ที่ `src/main/resources/db/migration/`

```bash
# Create new migration
# ตั้งชื่อ: V{version}__{description}.sql
# เช่น: V2__Add_user_table.sql
```

## 🐛 Troubleshooting

### Application ไม่สามารถเชื่อมต่อ Database

```bash
# ตรวจสอบว่า PostgreSQL รันอยู่
docker-compose ps

# ตรวจสอบ logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Redis connection error

```bash
# ตรวจสอบว่า Redis รันอยู่
docker-compose ps

# Test Redis connection
docker-compose exec redis redis-cli ping
# ควรได้ PONG

# Restart Redis
docker-compose restart redis
```

### Build errors

```bash
# Clean และ rebuild
mvn clean install -U

# Skip tests
mvn clean install -DskipTests
```

## 📝 TODO / Roadmap

- [ ] เพิ่ม OpenWeather Client สำหรับ multiple data sources
- [ ] Implement WeatherAggregator service สำหรับรวมข้อมูลจากหลาย sources
- [ ] เพิ่ม Unit tests coverage ให้ถึง 80%+
- [ ] เพิ่ม Integration tests
- [ ] Performance testing และ optimization
- [ ] Add authentication/authorization
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline setup

## 👥 Team & Development

Project นี้เป็นส่วนหนึ่งของ migration plan จาก Python FastAPI ไป Java Spring Boot

### Developer Assignment:
- **Developer 1**: External API clients, Business logic, Services
- **Developer 2**: REST controllers, Database, Caching, Testing

ดู [USER_STORIES.md](USER_STORIES.md) สำหรับ detailed task breakdown

## 📞 Support

สำหรับคำถามหรือปัญหา:
1. ตรวจสอบ [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
2. ดู API documentation ที่ Swagger UI
3. ตรวจสอบ logs: `docker-compose logs -f`

## 📄 License

[Your License Here]

---

**สร้างเมื่อ**: January 22, 2026  
**Status**: 🚀 Ready for Development  
**Version**: 1.0.0
