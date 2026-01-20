package repository

import (
	"database/sql"
	"fmt"

	"github.com/yourusername/blog-api/internal/models"
)

// TagRepository handles database operations for tags
type TagRepository struct {
	db *sql.DB
}

// NewTagRepository creates a new tag repository
func NewTagRepository(db *sql.DB) *TagRepository {
	return &TagRepository{db: db}
}

// Create creates a new tag
func (r *TagRepository) Create(tag *models.Tag) error {
	query := `INSERT INTO tags (name) VALUES (?)`
	result, err := r.db.Exec(query, tag.Name)
	if err != nil {
		return fmt.Errorf("failed to create tag: %w", err)
	}

	id, err := result.LastInsertId()
	if err != nil {
		return err
	}

	tag.ID = id
	return nil
}

// GetByName retrieves a tag by name
func (r *TagRepository) GetByName(name string) (*models.Tag, error) {
	query := `SELECT id, name FROM tags WHERE name = ?`

	tag := &models.Tag{}
	err := r.db.QueryRow(query, name).Scan(&tag.ID, &tag.Name)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get tag: %w", err)
	}

	return tag, nil
}

// GetOrCreate gets an existing tag or creates a new one
func (r *TagRepository) GetOrCreate(name string) (*models.Tag, error) {
	tag, err := r.GetByName(name)
	if err != nil {
		return nil, err
	}

	if tag != nil {
		return tag, nil
	}

	// Create new tag
	tag = &models.Tag{Name: name}
	if err := r.Create(tag); err != nil {
		return nil, err
	}

	return tag, nil
}

// List retrieves all tags
func (r *TagRepository) List() ([]models.Tag, error) {
	query := `SELECT id, name FROM tags ORDER BY name`

	rows, err := r.db.Query(query)
	if err != nil {
		return nil, fmt.Errorf("failed to list tags: %w", err)
	}
	defer rows.Close()

	var tags []models.Tag
	for rows.Next() {
		tag := models.Tag{}
		if err := rows.Scan(&tag.ID, &tag.Name); err != nil {
			return nil, err
		}
		tags = append(tags, tag)
	}

	return tags, nil
}
