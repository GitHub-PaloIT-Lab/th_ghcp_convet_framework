package com.weatherapi.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO for weather data from a single source
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WeatherSourceDto {

    private String source;
    private Double temperature;
    private Double humidity;
    private String description;
}
