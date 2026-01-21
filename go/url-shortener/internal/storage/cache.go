package storage

import (
	"database/sql"
	"time"
)

// Cache defines the interface for caching operations
type Cache interface {
	Get(key string) (string, error)
	Set(key string, value string, expiration time.Duration) error
	Delete(key string) error
}

// SQLiteCache implements the Cache interface using SQLite
type SQLiteCache struct {
	db *sql.DB
}

// NewSQLiteCache creates a new SQLite cache instance
func NewSQLiteCache(db *sql.DB) (*SQLiteCache, error) {
	// Create cache table
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS cache (
			key TEXT PRIMARY KEY,
			value TEXT NOT NULL,
			expires_at INTEGER NOT NULL
		)
	`)
	if err != nil {
		return nil, err
	}

	// Create index on expires_at for cleanup
	_, err = db.Exec(`CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache(expires_at)`)
	if err != nil {
		return nil, err
	}

	return &SQLiteCache{db: db}, nil
}

// Get retrieves a value from the cache
func (c *SQLiteCache) Get(key string) (string, error) {
	// Clean expired entries first
	c.cleanup()

	var value string
	err := c.db.QueryRow(
		"SELECT value FROM cache WHERE key = ? AND expires_at > ?",
		key, time.Now().Unix(),
	).Scan(&value)

	if err == sql.ErrNoRows {
		return "", nil // Key does not exist or expired
	}
	return value, err
}

// Set stores a value in the cache with expiration
func (c *SQLiteCache) Set(key string, value string, expiration time.Duration) error {
	expiresAt := time.Now().Add(expiration).Unix()
	_, err := c.db.Exec(
		"INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
		key, value, expiresAt,
	)
	return err
}

// Delete removes a key from the cache
func (c *SQLiteCache) Delete(key string) error {
	_, err := c.db.Exec("DELETE FROM cache WHERE key = ?", key)
	return err
}

// cleanup removes expired entries
func (c *SQLiteCache) cleanup() {
	c.db.Exec("DELETE FROM cache WHERE expires_at <= ?", time.Now().Unix())
}
