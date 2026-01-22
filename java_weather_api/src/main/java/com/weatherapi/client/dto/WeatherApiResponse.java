package com.weatherapi.client.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Response DTOs for WeatherAPI.com
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class WeatherApiResponse {

    private Location location;
    private Current current;
    private Forecast forecast;

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Location {
        private String name;
        private String region;
        private String country;
        private Double lat;
        private Double lon;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Current {
        @JsonProperty("temp_c")
        private Double tempC;
        
        @JsonProperty("feelslike_c")
        private Double feelslikeC;
        
        private Integer humidity;
        
        @JsonProperty("wind_kph")
        private Double windKph;
        
        private Condition condition;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Condition {
        private String text;
        private Integer code;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Forecast {
        @JsonProperty("forecastday")
        private java.util.List<ForecastDay> forecastday;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ForecastDay {
        private String date;
        private Day day;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Day {
        @JsonProperty("avgtemp_c")
        private Double avgtempC;
        
        @JsonProperty("maxtemp_c")
        private Double maxtempC;
        
        @JsonProperty("mintemp_c")
        private Double mintempC;
        
        @JsonProperty("avghumidity")
        private Double avghumidity;
        
        @JsonProperty("maxwind_kph")
        private Double maxwindKph;
        
        private Condition condition;
    }
}
