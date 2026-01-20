package handler

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/yourusername/url-shortener/internal/models"
	"github.com/yourusername/url-shortener/internal/service"
)

// URLHandler handles HTTP requests for URL operations
type URLHandler struct {
	service *service.URLService
}

// NewURLHandler creates a new URL handler
func NewURLHandler(service *service.URLService) *URLHandler {
	return &URLHandler{
		service: service,
	}
}

// CreateShortURL handles POST /api/urls
func (h *URLHandler) CreateShortURL(w http.ResponseWriter, r *http.Request) {
	var req models.CreateURLRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	// Get user ID from context (set by auth middleware)
	userID := r.Context().Value("userID").(string)

	url, err := h.service.CreateShortURL(req.OriginalURL, userID)
	if err != nil {
		respondError(w, http.StatusInternalServerError, err.Error())
		return
	}

	// Build response
	response := models.CreateURLResponse{
		ShortCode:   url.ShortCode,
		ShortURL:    "http://localhost:8080/" + url.ShortCode,
		OriginalURL: url.OriginalURL,
	}

	respondJSON(w, http.StatusCreated, response)
}

// RedirectURL handles GET /{shortCode}
func (h *URLHandler) RedirectURL(w http.ResponseWriter, r *http.Request) {
	shortCode := chi.URLParam(r, "shortCode")

	originalURL, err := h.service.GetOriginalURL(shortCode)
	if err != nil {
		respondError(w, http.StatusNotFound, "URL not found")
		return
	}

	// Record click
	referrer := r.Header.Get("Referer")
	go h.service.RecordClick(shortCode, referrer)

	http.Redirect(w, r, originalURL, http.StatusFound)
}

// ListURLs handles GET /api/urls
func (h *URLHandler) ListURLs(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("userID").(string)

	urls, err := h.service.ListUserURLs(userID)
	if err != nil {
		respondError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondJSON(w, http.StatusOK, urls)
}

// DeleteURL handles DELETE /api/urls/{shortCode}
func (h *URLHandler) DeleteURL(w http.ResponseWriter, r *http.Request) {
	shortCode := chi.URLParam(r, "shortCode")
	userID := r.Context().Value("userID").(string)

	if err := h.service.DeleteURL(shortCode, userID); err != nil {
		respondError(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.WriteHeader(http.StatusNoContent)
}
