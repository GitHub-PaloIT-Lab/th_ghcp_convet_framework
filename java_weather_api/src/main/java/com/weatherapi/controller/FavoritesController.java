package com.weatherapi.controller;

import com.weatherapi.dto.FavoriteDto;
import com.weatherapi.service.FavoritesService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * REST controller for managing favorite weather locations
 */
@RestController
@RequestMapping("/favorites")
@RequiredArgsConstructor
@Tag(name = "Favorites", description = "Manage favorite weather locations")
public class FavoritesController {

    private final FavoritesService favoritesService;

    @GetMapping
    @Operation(summary = "Get all favorite locations", description = "Returns a list of all saved favorite locations")
    public ResponseEntity<List<FavoriteDto>> getAllFavorites() {
        return ResponseEntity.ok(favoritesService.getAllFavorites());
    }

    @GetMapping("/{location}")
    @Operation(summary = "Get a favorite by location", description = "Returns details of a specific favorite location")
    public ResponseEntity<FavoriteDto> getFavorite(@PathVariable String location) {
        return ResponseEntity.ok(favoritesService.getFavoriteByLocation(location));
    }

    @PostMapping("/{location}")
    @Operation(summary = "Add a favorite location", description = "Adds a new location to favorites")
    public ResponseEntity<FavoriteDto> addFavorite(@PathVariable String location) {
        FavoriteDto favorite = favoritesService.addFavorite(location);
        return ResponseEntity.status(HttpStatus.CREATED).body(favorite);
    }

    @DeleteMapping("/{location}")
    @Operation(summary = "Remove a favorite location", description = "Removes a location from favorites")
    public ResponseEntity<Map<String, String>> removeFavorite(@PathVariable String location) {
        favoritesService.removeFavorite(location);
        return ResponseEntity.ok(Map.of(
                "message", "Favorite removed successfully",
                "location", location
        ));
    }

    @GetMapping("/{location}/exists")
    @Operation(summary = "Check if location is favorite", description = "Checks if a location exists in favorites")
    public ResponseEntity<Map<String, Boolean>> checkFavorite(@PathVariable String location) {
        boolean exists = favoritesService.isFavorite(location);
        return ResponseEntity.ok(Map.of("exists", exists));
    }
}
