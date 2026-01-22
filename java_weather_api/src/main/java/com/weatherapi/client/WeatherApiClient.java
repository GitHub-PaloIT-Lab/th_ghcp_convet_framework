package com.weatherapi.client;

import com.weatherapi.client.dto.WeatherApiResponse;
import com.weatherapi.config.WeatherApiProperties;
import com.weatherapi.dto.ForecastDto;
import com.weatherapi.dto.WeatherDto;
import com.weatherapi.dto.WeatherSourceDto;
import com.weatherapi.exception.ExternalApiException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Client for WeatherAPI.com API
 * Fetches weather data from WeatherAPI.com
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class WeatherApiClient {

    private final WebClient.Builder webClientBuilder;
    private final WeatherApiProperties properties;

    /**
     * Get current weather for a location
     * 
     * @param location the location to get weather for
     * @return weather data with source information
     */
    public WeatherDto getCurrentWeather(String location) {
        log.debug("Fetching current weather from WeatherAPI.com for: {}", location);

        String baseUrl = properties.getWeatherApiBaseUrl();
        String apiKey = properties.getWeatherApiKey();

        try {
            WeatherApiResponse response = webClientBuilder.build()
                    .get()
                    .uri(baseUrl + "/current.json?key={key}&q={location}", apiKey, location)
                    .retrieve()
                    .bodyToMono(WeatherApiResponse.class)
                    .retryWhen(Retry.backoff(properties.getMaxRetries(), Duration.ofSeconds(1)))
                    .timeout(Duration.ofSeconds(properties.getTimeoutSeconds()))
                    .block();

            if (response == null || response.getCurrent() == null) {
                throw new ExternalApiException("Empty response from WeatherAPI.com");
            }

            return convertToWeatherDto(response);

        } catch (Exception e) {
            log.error("Error fetching weather from WeatherAPI.com: {}", e.getMessage());
            throw new ExternalApiException("Failed to fetch weather from WeatherAPI.com: " + e.getMessage(), e);
        }
    }

    /**
     * Get weather forecast for a location
     * 
     * @param location the location to get forecast for
     * @param days number of days to forecast (1-7)
     * @return list of forecast data
     */
    public List<ForecastDto> getForecast(String location, int days) {
        log.debug("Fetching {}-day forecast from WeatherAPI.com for: {}", days, location);

        String baseUrl = properties.getWeatherApiBaseUrl();
        String apiKey = properties.getWeatherApiKey();

        try {
            WeatherApiResponse response = webClientBuilder.build()
                    .get()
                    .uri(baseUrl + "/forecast.json?key={key}&q={location}&days={days}", 
                         apiKey, location, days)
                    .retrieve()
                    .bodyToMono(WeatherApiResponse.class)
                    .retryWhen(Retry.backoff(properties.getMaxRetries(), Duration.ofSeconds(1)))
                    .timeout(Duration.ofSeconds(properties.getTimeoutSeconds()))
                    .block();

            if (response == null || response.getForecast() == null) {
                throw new ExternalApiException("Empty forecast response from WeatherAPI.com");
            }

            return response.getForecast().getForecastday().stream()
                    .map(this::convertToForecastDto)
                    .collect(Collectors.toList());

        } catch (Exception e) {
            log.error("Error fetching forecast from WeatherAPI.com: {}", e.getMessage());
            throw new ExternalApiException("Failed to fetch forecast from WeatherAPI.com: " + e.getMessage(), e);
        }
    }

    /**
     * Convert WeatherAPI response to WeatherDto
     */
    private WeatherDto convertToWeatherDto(WeatherApiResponse response) {
        WeatherSourceDto source = WeatherSourceDto.builder()
                .source("WeatherAPI.com")
                .temperature(response.getCurrent().getTempC())
                .humidity(response.getCurrent().getHumidity().doubleValue())
                .description(response.getCurrent().getCondition().getText())
                .build();

        return WeatherDto.builder()
                .location(response.getLocation().getName())
                .avgTemperature(response.getCurrent().getTempC())
                .avgHumidity(response.getCurrent().getHumidity().doubleValue())
                .consensusDescription(response.getCurrent().getCondition().getText())
                .sources(List.of(source))
                .timestamp(LocalDateTime.now())
                .build();
    }

    /**
     * Convert forecast day to ForecastDto
     */
    private ForecastDto convertToForecastDto(WeatherApiResponse.ForecastDay forecastDay) {
        return ForecastDto.builder()
                .date(LocalDate.parse(forecastDay.getDate(), DateTimeFormatter.ISO_DATE))
                .avgTemperature(forecastDay.getDay().getAvgtempC())
                .minTemperature(forecastDay.getDay().getMintempC())
                .maxTemperature(forecastDay.getDay().getMaxtempC())
                .avgHumidity(forecastDay.getDay().getAvghumidity())
                .description(forecastDay.getDay().getCondition().getText())
                .build();
    }
}
