package com.weatherapi.service;

import com.weatherapi.dto.FavoriteDto;
import com.weatherapi.entity.Favorite;
import com.weatherapi.exception.ResourceNotFoundException;
import com.weatherapi.repository.FavoriteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service for managing favorite weather locations
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class FavoritesService {

    private final FavoriteRepository favoriteRepository;

    /**
     * Get all favorite locations
     * 
     * @return list of all favorites
     */
    public List<FavoriteDto> getAllFavorites() {
        log.debug("Fetching all favorites");
        return favoriteRepository.findAll().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    /**
     * Get a favorite by location
     * 
     * @param location the location name
     * @return the favorite DTO
     * @throws ResourceNotFoundException if location not found
     */
    public FavoriteDto getFavoriteByLocation(String location) {
        log.debug("Fetching favorite for location: {}", location);
        return favoriteRepository.findByLocation(location)
                .map(this::convertToDto)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Favorite location not found: " + location));
    }

    /**
     * Add a new favorite location
     * 
     * @param location the location to add
     * @return the created favorite DTO
     */
    @Transactional
    public FavoriteDto addFavorite(String location) {
        log.info("Adding favorite location: {}", location);
        
        // Check if already exists
        if (favoriteRepository.existsByLocation(location)) {
            log.debug("Location already exists in favorites: {}", location);
            return getFavoriteByLocation(location);
        }

        Favorite favorite = Favorite.builder()
                .location(location)
                .build();
        
        Favorite saved = favoriteRepository.save(favorite);
        log.info("Successfully added favorite: {}", location);
        
        return convertToDto(saved);
    }

    /**
     * Remove a favorite location
     * 
     * @param location the location to remove
     * @throws ResourceNotFoundException if location not found
     */
    @Transactional
    public void removeFavorite(String location) {
        log.info("Removing favorite location: {}", location);
        
        if (!favoriteRepository.existsByLocation(location)) {
            throw new ResourceNotFoundException("Favorite location not found: " + location);
        }
        
        favoriteRepository.deleteByLocation(location);
        log.info("Successfully removed favorite: {}", location);
    }

    /**
     * Check if a location is in favorites
     * 
     * @param location the location to check
     * @return true if exists, false otherwise
     */
    public boolean isFavorite(String location) {
        return favoriteRepository.existsByLocation(location);
    }

    /**
     * Convert Favorite entity to DTO
     */
    private FavoriteDto convertToDto(Favorite favorite) {
        return FavoriteDto.builder()
                .id(favorite.getId())
                .location(favorite.getLocation())
                .createdAt(favorite.getCreatedAt())
                .updatedAt(favorite.getUpdatedAt())
                .build();
    }
}
