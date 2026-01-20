package service

import (
	"fmt"

	"github.com/yourusername/url-shortener/internal/models"
	"github.com/yourusername/url-shortener/internal/storage"
)

// AnalyticsService handles analytics operations
type AnalyticsService struct {
	store storage.Store
}

// NewAnalyticsService creates a new analytics service
func NewAnalyticsService(store storage.Store) *AnalyticsService {
	return &AnalyticsService{
		store: store,
	}
}

// GetAnalytics retrieves analytics for a short code
func (s *AnalyticsService) GetAnalytics(shortCode string) (*models.Analytics, error) {
	// Get URL
	url, err := s.store.GetURL(shortCode)
	if err != nil {
		return nil, fmt.Errorf("failed to get URL: %w", err)
	}
	if url == nil {
		return nil, fmt.Errorf("URL not found")
	}

	// Get click count
	count, err := s.store.GetClickCount(shortCode)
	if err != nil {
		return nil, fmt.Errorf("failed to get click count: %w", err)
	}

	// Get recent clicks
	clicks, err := s.store.GetRecentClicks(shortCode, 10)
	if err != nil {
		return nil, fmt.Errorf("failed to get recent clicks: %w", err)
	}

	analytics := &models.Analytics{
		ShortCode:   url.ShortCode,
		OriginalURL: url.OriginalURL,
		TotalClicks: count,
		Clicks:      clicks,
		CreatedAt:   url.CreatedAt.Format("2006-01-02 15:04:05"),
	}

	return analytics, nil
}
