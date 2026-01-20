package models

// Analytics represents analytics data for a shortened URL
type Analytics struct {
	ShortCode   string  `json:"short_code"`
	OriginalURL string  `json:"original_url"`
	TotalClicks int     `json:"total_clicks"`
	Clicks      []Click `json:"recent_clicks"`
	CreatedAt   string  `json:"created_at"`
}
