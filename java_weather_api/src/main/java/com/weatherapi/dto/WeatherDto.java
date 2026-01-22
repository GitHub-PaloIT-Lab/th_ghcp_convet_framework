package com.weatherapi.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * DTO for aggregated weather data from multiple sources
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WeatherDto {

    private String location;

    @JsonProperty("avg_temperature")
    private Double avgTemperature;

    @JsonProperty("avg_humidity")
    private Double avgHumidity;

    @JsonProperty("consensus_description")
    private String consensusDescription;

    private List<WeatherSourceDto> sources;

    private LocalDateTime timestamp;
}
