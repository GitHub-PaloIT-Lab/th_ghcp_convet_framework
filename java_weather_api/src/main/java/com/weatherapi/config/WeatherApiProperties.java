package com.weatherapi.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration properties for external weather APIs
 */
@Configuration
@ConfigurationProperties(prefix = "weather.api")
@Data
public class WeatherApiProperties {

    private String weatherApiKey;
    private String openWeatherApiKey;
    private String weatherApiBaseUrl = "https://api.weatherapi.com/v1";
    private String openWeatherBaseUrl = "https://api.openweathermap.org/data/2.5";
    private int timeoutSeconds = 30;
    private int maxRetries = 3;
}
