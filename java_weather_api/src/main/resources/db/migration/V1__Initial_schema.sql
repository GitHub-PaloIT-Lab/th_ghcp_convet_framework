-- Initial database schema for Weather API
-- Creates favorites table for storing user's favorite locations

CREATE TABLE IF NOT EXISTS favorites (
    id BIGSERIAL PRIMARY KEY,
    location VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on location for faster lookups
CREATE INDEX idx_favorites_location ON favorites(location);

-- Create index on created_at for sorting
CREATE INDEX idx_favorites_created_at ON favorites(created_at DESC);

-- Add comments for documentation
COMMENT ON TABLE favorites IS 'Stores user favorite weather locations';
COMMENT ON COLUMN favorites.id IS 'Primary key';
COMMENT ON COLUMN favorites.location IS 'City or location name (unique)';
COMMENT ON COLUMN favorites.created_at IS 'Timestamp when favorite was added';
COMMENT ON COLUMN favorites.updated_at IS 'Timestamp when favorite was last updated';
