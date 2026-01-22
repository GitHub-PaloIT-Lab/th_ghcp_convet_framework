package com.weatherapi.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

/**
 * DTO for forecast data
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ForecastDto {

    private LocalDate date;

    @JsonProperty("avg_temperature")
    private Double avgTemperature;

    @JsonProperty("min_temperature")
    private Double minTemperature;

    @JsonProperty("max_temperature")
    private Double maxTemperature;

    @JsonProperty("avg_humidity")
    private Double avgHumidity;

    private String description;
}
