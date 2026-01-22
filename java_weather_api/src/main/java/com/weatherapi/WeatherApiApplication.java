package com.weatherapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * Main Spring Boot application class for Weather API
 * 
 * This application aggregates weather data from multiple sources:
 * - WeatherAPI.com
 * - OpenWeatherMap
 * 
 * Features:
 * - Current weather data retrieval
 * - Weather forecasts
 * - City comparison
 * - Favorites management
 * - Redis caching
 * - PostgreSQL persistence
 */
@SpringBootApplication
@EnableCaching
@EnableJpaRepositories
public class WeatherApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(WeatherApiApplication.class, args);
    }
}
