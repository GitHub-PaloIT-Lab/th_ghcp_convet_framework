package storage

import (
	"database/sql"
	"fmt"
	"time"

	_ "github.com/mattn/go-sqlite3"
	"github.com/yourusername/url-shortener/internal/models"
)

// Store defines the interface for database operations
type Store interface {
	CreateURL(url *models.URL) error
	GetURL(shortCode string) (*models.URL, error)
	GetUserURLs(userID string) ([]*models.URL, error)
	DeleteURL(shortCode string) error
	RecordClick(shortCode string, referrer string) error
	GetClickCount(shortCode string) (int, error)
	GetRecentClicks(shortCode string, limit int) ([]models.Click, error)
	Close() error
}

// SQLiteStore implements the Store interface using SQLite
type SQLiteStore struct {
	db *sql.DB
}

// NewSQLiteStore creates a new SQLite store instance
func NewSQLiteStore(dbPath string) (*SQLiteStore, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// Create tables
	if err := createTables(db); err != nil {
		return nil, fmt.Errorf("failed to create tables: %w", err)
	}

	return &SQLiteStore{db: db}, nil
}

func createTables(db *sql.DB) error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS urls (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			short_code TEXT UNIQUE NOT NULL,
			original_url TEXT NOT NULL,
			user_id TEXT NOT NULL,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS clicks (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			short_code TEXT NOT NULL,
			clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			referrer TEXT,
			FOREIGN KEY (short_code) REFERENCES urls(short_code) ON DELETE CASCADE
		)`,
		`CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)`,
		`CREATE INDEX IF NOT EXISTS idx_user_id ON urls(user_id)`,
		`CREATE INDEX IF NOT EXISTS idx_clicks_short_code ON clicks(short_code)`,
	}

	for _, query := range queries {
		if _, err := db.Exec(query); err != nil {
			return err
		}
	}

	return nil
}

// CreateURL creates a new shortened URL
func (s *SQLiteStore) CreateURL(url *models.URL) error {
	query := `INSERT INTO urls (short_code, original_url, user_id) VALUES (?, ?, ?)`
	result, err := s.db.Exec(query, url.ShortCode, url.OriginalURL, url.UserID)
	if err != nil {
		return fmt.Errorf("failed to create URL: %w", err)
	}

	id, err := result.LastInsertId()
	if err != nil {
		return err
	}

	url.ID = id
	url.CreatedAt = time.Now()
	return nil
}

// GetURL retrieves a URL by short code
func (s *SQLiteStore) GetURL(shortCode string) (*models.URL, error) {
	query := `SELECT id, short_code, original_url, user_id, created_at FROM urls WHERE short_code = ?`

	url := &models.URL{}
	err := s.db.QueryRow(query, shortCode).Scan(
		&url.ID,
		&url.ShortCode,
		&url.OriginalURL,
		&url.UserID,
		&url.CreatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get URL: %w", err)
	}

	return url, nil
}

// GetUserURLs retrieves all URLs for a user
func (s *SQLiteStore) GetUserURLs(userID string) ([]*models.URL, error) {
	query := `SELECT id, short_code, original_url, user_id, created_at FROM urls WHERE user_id = ? ORDER BY created_at DESC`

	rows, err := s.db.Query(query, userID)
	if err != nil {
		return nil, fmt.Errorf("failed to get user URLs: %w", err)
	}
	defer rows.Close()

	var urls []*models.URL
	for rows.Next() {
		url := &models.URL{}
		if err := rows.Scan(&url.ID, &url.ShortCode, &url.OriginalURL, &url.UserID, &url.CreatedAt); err != nil {
			return nil, err
		}
		urls = append(urls, url)
	}

	return urls, nil
}

// DeleteURL deletes a URL by short code
func (s *SQLiteStore) DeleteURL(shortCode string) error {
	query := `DELETE FROM urls WHERE short_code = ?`
	_, err := s.db.Exec(query, shortCode)
	if err != nil {
		return fmt.Errorf("failed to delete URL: %w", err)
	}
	return nil
}

// RecordClick records a click event
func (s *SQLiteStore) RecordClick(shortCode string, referrer string) error {
	query := `INSERT INTO clicks (short_code, referrer) VALUES (?, ?)`
	_, err := s.db.Exec(query, shortCode, referrer)
	if err != nil {
		return fmt.Errorf("failed to record click: %w", err)
	}
	return nil
}

// GetClickCount gets the total click count for a short code
func (s *SQLiteStore) GetClickCount(shortCode string) (int, error) {
	query := `SELECT COUNT(*) FROM clicks WHERE short_code = ?`

	var count int
	err := s.db.QueryRow(query, shortCode).Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("failed to get click count: %w", err)
	}

	return count, nil
}

// GetRecentClicks gets recent clicks for a short code
func (s *SQLiteStore) GetRecentClicks(shortCode string, limit int) ([]models.Click, error) {
	query := `SELECT id, short_code, clicked_at, referrer FROM clicks WHERE short_code = ? ORDER BY clicked_at DESC LIMIT ?`

	rows, err := s.db.Query(query, shortCode, limit)
	if err != nil {
		return nil, fmt.Errorf("failed to get recent clicks: %w", err)
	}
	defer rows.Close()

	var clicks []models.Click
	for rows.Next() {
		click := models.Click{}
		if err := rows.Scan(&click.ID, &click.ShortCode, &click.ClickedAt, &click.Referrer); err != nil {
			return nil, err
		}
		clicks = append(clicks, click)
	}

	return clicks, nil
}

// Close closes the database connection
func (s *SQLiteStore) Close() error {
	return s.db.Close()
}

// DB returns the underlying database connection
func (s *SQLiteStore) DB() *sql.DB {
	return s.db
}
