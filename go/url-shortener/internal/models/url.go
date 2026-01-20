package models

import "time"

// URL represents a shortened URL
type URL struct {
	ID          int64     `json:"id"`
	ShortCode   string    `json:"short_code"`
	OriginalURL string    `json:"original_url"`
	UserID      string    `json:"user_id"`
	CreatedAt   time.Time `json:"created_at"`
}

// Click represents a click event on a shortened URL
type Click struct {
	ID        int64     `json:"id"`
	ShortCode string    `json:"short_code"`
	ClickedAt time.Time `json:"clicked_at"`
	Referrer  string    `json:"referrer,omitempty"`
}

// CreateURLRequest is the request body for creating a short URL
type CreateURLRequest struct {
	OriginalURL string `json:"original_url"`
}

// CreateURLResponse is the response body for creating a short URL
type CreateURLResponse struct {
	ShortCode   string `json:"short_code"`
	ShortURL    string `json:"short_url"`
	OriginalURL string `json:"original_url"`
}
