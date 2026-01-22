package com.weatherapi.repository;

import com.weatherapi.entity.Favorite;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository interface for Favorite entity
 * Provides CRUD operations for favorite locations
 */
@Repository
public interface FavoriteRepository extends JpaRepository<Favorite, Long> {

    /**
     * Find a favorite by location name
     * 
     * @param location the location name to search for
     * @return Optional containing the favorite if found
     */
    Optional<Favorite> findByLocation(String location);

    /**
     * Check if a location exists in favorites
     * 
     * @param location the location name to check
     * @return true if the location exists, false otherwise
     */
    boolean existsByLocation(String location);

    /**
     * Delete a favorite by location name
     * 
     * @param location the location name to delete
     */
    void deleteByLocation(String location);
}
