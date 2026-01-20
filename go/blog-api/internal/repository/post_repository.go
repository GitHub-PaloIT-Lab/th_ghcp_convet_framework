package repository

import (
	"database/sql"
	"fmt"
	"strings"

	"github.com/yourusername/blog-api/internal/models"
)

// PostRepository handles database operations for posts
type PostRepository struct {
	db *sql.DB
}

// NewPostRepository creates a new post repository
func NewPostRepository(db *sql.DB) *PostRepository {
	return &PostRepository{db: db}
}

// Create creates a new post
func (r *PostRepository) Create(post *models.Post) error {
	query := `INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)`
	result, err := r.db.Exec(query, post.Title, post.Content, post.AuthorID)
	if err != nil {
		return fmt.Errorf("failed to create post: %w", err)
	}

	id, err := result.LastInsertId()
	if err != nil {
		return err
	}

	post.ID = id
	return nil
}

// GetByID retrieves a post by ID
func (r *PostRepository) GetByID(id int64) (*models.Post, error) {
	query := `
		SELECT p.id, p.title, p.content, p.author_id, p.created_at, p.updated_at,
		       u.id, u.username, u.email, u.created_at
		FROM posts p
		JOIN users u ON p.author_id = u.id
		WHERE p.id = ?
	`

	post := &models.Post{Author: &models.User{}}
	err := r.db.QueryRow(query, id).Scan(
		&post.ID,
		&post.Title,
		&post.Content,
		&post.AuthorID,
		&post.CreatedAt,
		&post.UpdatedAt,
		&post.Author.ID,
		&post.Author.Username,
		&post.Author.Email,
		&post.Author.CreatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get post: %w", err)
	}

	return post, nil
}

// List retrieves posts with pagination
func (r *PostRepository) List(limit, offset int) ([]*models.Post, error) {
	query := `
		SELECT p.id, p.title, p.content, p.author_id, p.created_at, p.updated_at,
		       u.id, u.username, u.email, u.created_at
		FROM posts p
		JOIN users u ON p.author_id = u.id
		ORDER BY p.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := r.db.Query(query, limit, offset)
	if err != nil {
		return nil, fmt.Errorf("failed to list posts: %w", err)
	}
	defer rows.Close()

	var posts []*models.Post
	for rows.Next() {
		post := &models.Post{Author: &models.User{}}
		if err := rows.Scan(
			&post.ID,
			&post.Title,
			&post.Content,
			&post.AuthorID,
			&post.CreatedAt,
			&post.UpdatedAt,
			&post.Author.ID,
			&post.Author.Username,
			&post.Author.Email,
			&post.Author.CreatedAt,
		); err != nil {
			return nil, err
		}
		posts = append(posts, post)
	}

	return posts, nil
}

// Update updates a post
func (r *PostRepository) Update(post *models.Post) error {
	query := `UPDATE posts SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`
	_, err := r.db.Exec(query, post.Title, post.Content, post.ID)
	if err != nil {
		return fmt.Errorf("failed to update post: %w", err)
	}
	return nil
}

// Delete deletes a post
func (r *PostRepository) Delete(id int64) error {
	query := `DELETE FROM posts WHERE id = ?`
	_, err := r.db.Exec(query, id)
	if err != nil {
		return fmt.Errorf("failed to delete post: %w", err)
	}
	return nil
}

// Search searches posts by title or content
func (r *PostRepository) Search(query string) ([]*models.Post, error) {
	searchQuery := `
		SELECT p.id, p.title, p.content, p.author_id, p.created_at, p.updated_at,
		       u.id, u.username, u.email, u.created_at
		FROM posts p
		JOIN users u ON p.author_id = u.id
		WHERE p.title LIKE ? OR p.content LIKE ?
		ORDER BY p.created_at DESC
	`

	searchTerm := "%" + query + "%"
	rows, err := r.db.Query(searchQuery, searchTerm, searchTerm)
	if err != nil {
		return nil, fmt.Errorf("failed to search posts: %w", err)
	}
	defer rows.Close()

	var posts []*models.Post
	for rows.Next() {
		post := &models.Post{Author: &models.User{}}
		if err := rows.Scan(
			&post.ID,
			&post.Title,
			&post.Content,
			&post.AuthorID,
			&post.CreatedAt,
			&post.UpdatedAt,
			&post.Author.ID,
			&post.Author.Username,
			&post.Author.Email,
			&post.Author.CreatedAt,
		); err != nil {
			return nil, err
		}
		posts = append(posts, post)
	}

	return posts, nil
}

// ListByTag retrieves posts with a specific tag
func (r *PostRepository) ListByTag(tagID int64, limit, offset int) ([]*models.Post, error) {
	query := `
		SELECT p.id, p.title, p.content, p.author_id, p.created_at, p.updated_at,
		       u.id, u.username, u.email, u.created_at
		FROM posts p
		JOIN users u ON p.author_id = u.id
		JOIN post_tags pt ON p.id = pt.post_id
		WHERE pt.tag_id = ?
		ORDER BY p.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := r.db.Query(query, tagID, limit, offset)
	if err != nil {
		return nil, fmt.Errorf("failed to list posts by tag: %w", err)
	}
	defer rows.Close()

	var posts []*models.Post
	for rows.Next() {
		post := &models.Post{Author: &models.User{}}
		if err := rows.Scan(
			&post.ID,
			&post.Title,
			&post.Content,
			&post.AuthorID,
			&post.CreatedAt,
			&post.UpdatedAt,
			&post.Author.ID,
			&post.Author.Username,
			&post.Author.Email,
			&post.Author.CreatedAt,
		); err != nil {
			return nil, err
		}
		posts = append(posts, post)
	}

	return posts, nil
}

// AddTags adds tags to a post
func (r *PostRepository) AddTags(postID int64, tagIDs []int64) error {
	if len(tagIDs) == 0 {
		return nil
	}

	// Clear existing tags
	_, err := r.db.Exec(`DELETE FROM post_tags WHERE post_id = ?`, postID)
	if err != nil {
		return fmt.Errorf("failed to clear existing tags: %w", err)
	}

	// Insert new tags
	values := make([]string, len(tagIDs))
	args := make([]interface{}, 0, len(tagIDs)*2)
	for i, tagID := range tagIDs {
		values[i] = "(?, ?)"
		args = append(args, postID, tagID)
	}

	query := `INSERT INTO post_tags (post_id, tag_id) VALUES ` + strings.Join(values, ", ")
	_, err = r.db.Exec(query, args...)
	if err != nil {
		return fmt.Errorf("failed to add tags: %w", err)
	}

	return nil
}

// GetPostTags retrieves tags for a post
func (r *PostRepository) GetPostTags(postID int64) ([]models.Tag, error) {
	query := `
		SELECT t.id, t.name
		FROM tags t
		JOIN post_tags pt ON t.id = pt.tag_id
		WHERE pt.post_id = ?
	`

	rows, err := r.db.Query(query, postID)
	if err != nil {
		return nil, fmt.Errorf("failed to get post tags: %w", err)
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
