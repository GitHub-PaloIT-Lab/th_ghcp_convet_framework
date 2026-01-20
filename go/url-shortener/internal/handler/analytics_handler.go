package handler

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/yourusername/url-shortener/internal/service"
)

// AnalyticsHandler handles HTTP requests for analytics operations
type AnalyticsHandler struct {
	service *service.AnalyticsService
}

// NewAnalyticsHandler creates a new analytics handler
func NewAnalyticsHandler(service *service.AnalyticsService) *AnalyticsHandler {
	return &AnalyticsHandler{
		service: service,
	}
}

// GetAnalytics handles GET /api/analytics/{shortCode}
func (h *AnalyticsHandler) GetAnalytics(w http.ResponseWriter, r *http.Request) {
	shortCode := chi.URLParam(r, "shortCode")

	analytics, err := h.service.GetAnalytics(shortCode)
	if err != nil {
		respondError(w, http.StatusNotFound, err.Error())
		return
	}

	respondJSON(w, http.StatusOK, analytics)
}
