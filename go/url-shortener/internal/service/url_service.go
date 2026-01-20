package service

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"time"

	"github.com/yourusername/url-shortener/internal/models"
	"github.com/yourusername/url-shortener/internal/storage"
)

// URLService handles business logic for URL operations
type URLService struct {
	cache storage.Cache
	store storage.Store
}

// NewURLService creates a new URL service
func NewURLService(cache storage.Cache, store storage.Store) *URLService {
	return &URLService{
		cache: cache,
		store: store,
	}
}

// CreateShortURL creates a new shortened URL
func (s *URLService) CreateShortURL(originalURL string, userID string) (*models.URL, error) {
	// Validate URL
	if originalURL == "" {
		return nil, fmt.Errorf("original URL cannot be empty")
	}

	// Generate short code
	shortCode := s.generateShortCode()

	// Create URL
	url := &models.URL{
		ShortCode:   shortCode,
		OriginalURL: originalURL,
		UserID:      userID,
	}

	if err := s.store.CreateURL(url); err != nil {
		return nil, fmt.Errorf("failed to create short URL: %w", err)
	}

	// Cache the URL
	s.cache.Set(shortCode, originalURL, 24*time.Hour)

	return url, nil
}

// GetOriginalURL retrieves the original URL from a short code
func (s *URLService) GetOriginalURL(shortCode string) (string, error) {
	// Try cache first
	if cached, err := s.cache.Get(shortCode); err == nil && cached != "" {
		return cached, nil
	}

	// Fallback to database
	url, err := s.store.GetURL(shortCode)
	if err != nil {
		return "", fmt.Errorf("failed to get URL: %w", err)
	}
	if url == nil {
		return "", fmt.Errorf("URL not found")
	}

	// Update cache
	s.cache.Set(shortCode, url.OriginalURL, 24*time.Hour)

	return url.OriginalURL, nil
}

// ListUserURLs retrieves all URLs for a user
func (s *URLService) ListUserURLs(userID string) ([]*models.URL, error) {
	urls, err := s.store.GetUserURLs(userID)
	if err != nil {
		return nil, fmt.Errorf("failed to list URLs: %w", err)
	}
	return urls, nil
}

// DeleteURL deletes a shortened URL
func (s *URLService) DeleteURL(shortCode string, userID string) error {
	// Verify ownership
	url, err := s.store.GetURL(shortCode)
	if err != nil {
		return fmt.Errorf("failed to get URL: %w", err)
	}
	if url == nil {
		return fmt.Errorf("URL not found")
	}
	if url.UserID != userID {
		return fmt.Errorf("unauthorized: URL belongs to different user")
	}

	// Delete from database
	if err := s.store.DeleteURL(shortCode); err != nil {
		return fmt.Errorf("failed to delete URL: %w", err)
	}

	// Delete from cache
	s.cache.Delete(shortCode)

	return nil
}

// RecordClick records a click event
func (s *URLService) RecordClick(shortCode string, referrer string) error {
	return s.store.RecordClick(shortCode, referrer)
}

// generateShortCode generates a random short code
func (s *URLService) generateShortCode() string {
	b := make([]byte, 6)
	rand.Read(b)
	return base64.URLEncoding.EncodeToString(b)[:8]
}
