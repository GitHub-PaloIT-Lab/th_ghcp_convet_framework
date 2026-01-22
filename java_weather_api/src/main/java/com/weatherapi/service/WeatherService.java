package com.weatherapi.service;

import com.weatherapi.client.WeatherApiClient;
import com.weatherapi.dto.ForecastDto;
import com.weatherapi.dto.WeatherDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Service for weather operations
 * Handles weather data retrieval and aggregation
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class WeatherService {

    private final WeatherApiClient weatherApiClient;

    /**
     * Get current weather for a location
     * Results are cached for 30 minutes
     * 
     * @param location the location to get weather for
     * @return aggregated weather data
     */
    @Cacheable(value = "weather", key = "#location")
    public WeatherDto getCurrentWeather(String location) {
        log.info("Fetching current weather for: {}", location);
        return weatherApiClient.getCurrentWeather(location);
    }

    /**
     * Get weather forecast for a location
     * Results are cached for 30 minutes
     * 
     * @param location the location to get forecast for
     * @param days number of days to forecast (default: 5, max: 7)
     * @return list of forecast data
     */
    @Cacheable(value = "forecast", key = "#location + '-' + #days")
    public List<ForecastDto> getForecast(String location, int days) {
        log.info("Fetching {}-day forecast for: {}", days, location);
        
        // Validate days parameter
        if (days < 1 || days > 7) {
            log.warn("Invalid days parameter: {}. Using default value of 5", days);
            days = 5;
        }
        
        return weatherApiClient.getForecast(location, days);
    }

    /**
     * Compare weather across multiple locations
     * 
     * @param locations list of locations to compare
     * @return list of weather data for each location
     */
    public List<WeatherDto> compareWeather(List<String> locations) {
        log.info("Comparing weather for {} locations", locations.size());
        
        return locations.stream()
                .map(this::getCurrentWeather)
                .toList();
    }
}
