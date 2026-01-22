package com.weatherapi.controller;

import com.weatherapi.dto.ForecastDto;
import com.weatherapi.dto.WeatherDto;
import com.weatherapi.service.WeatherService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * REST controller for weather operations
 */
@RestController
@RequestMapping("/weather")
@RequiredArgsConstructor
@Tag(name = "Weather", description = "Weather data operations")
public class WeatherController {

    private final WeatherService weatherService;

    @GetMapping("/current/{location}")
    @Operation(summary = "Get current weather", description = "Returns current weather data for a specific location")
    public ResponseEntity<WeatherDto> getCurrentWeather(
            @Parameter(description = "Location name (city, coordinates, etc.)")
            @PathVariable String location) {
        return ResponseEntity.ok(weatherService.getCurrentWeather(location));
    }

    @GetMapping("/forecast/{location}")
    @Operation(summary = "Get weather forecast", description = "Returns weather forecast for a specific location")
    public ResponseEntity<List<ForecastDto>> getForecast(
            @Parameter(description = "Location name")
            @PathVariable String location,
            @Parameter(description = "Number of days (1-7, default: 5)")
            @RequestParam(defaultValue = "5") int days) {
        return ResponseEntity.ok(weatherService.getForecast(location, days));
    }

    @PostMapping("/compare")
    @Operation(summary = "Compare weather", description = "Compares weather across multiple locations")
    public ResponseEntity<List<WeatherDto>> compareWeather(
            @RequestBody Map<String, List<String>> request) {
        List<String> locations = request.get("locations");
        
        if (locations == null || locations.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }
        
        return ResponseEntity.ok(weatherService.compareWeather(locations));
    }
}
