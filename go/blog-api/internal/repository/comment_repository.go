package repository

import (
	"database/sql"
	"fmt"

	"github.com/yourusername/blog-api/internal/models"
)

// CommentRepository handles database operations for comments
type CommentRepository struct {
	db *sql.DB
}

// NewCommentRepository creates a new comment repository
func NewCommentRepository(db *sql.DB) *CommentRepository {
	return &CommentRepository{db: db}
}

// Create creates a new comment
func (r *CommentRepository) Create(comment *models.Comment) error {
	query := `INSERT INTO comments (post_id, author_id, content) VALUES (?, ?, ?)`
	result, err := r.db.Exec(query, comment.PostID, comment.AuthorID, comment.Content)
	if err != nil {
		return fmt.Errorf("failed to create comment: %w", err)
	}

	id, err := result.LastInsertId()
	if err != nil {
		return err
	}

	comment.ID = id
	return nil
}

// GetByPostID retrieves all comments for a post
func (r *CommentRepository) GetByPostID(postID int64) ([]models.Comment, error) {
	query := `
		SELECT c.id, c.post_id, c.author_id, c.content, c.created_at,
		       u.id, u.username, u.email, u.created_at
		FROM comments c
		JOIN users u ON c.author_id = u.id
		WHERE c.post_id = ?
		ORDER BY c.created_at DESC
	`

	rows, err := r.db.Query(query, postID)
	if err != nil {
		return nil, fmt.Errorf("failed to get comments: %w", err)
	}
	defer rows.Close()

	var comments []models.Comment
	for rows.Next() {
		comment := models.Comment{Author: &models.User{}}
		if err := rows.Scan(
			&comment.ID,
			&comment.PostID,
			&comment.AuthorID,
			&comment.Content,
			&comment.CreatedAt,
			&comment.Author.ID,
			&comment.Author.Username,
			&comment.Author.Email,
			&comment.Author.CreatedAt,
		); err != nil {
			return nil, err
		}
		comments = append(comments, comment)
	}

	return comments, nil
}

// Delete deletes a comment
func (r *CommentRepository) Delete(id int64) error {
	query := `DELETE FROM comments WHERE id = ?`
	_, err := r.db.Exec(query, id)
	if err != nil {
		return fmt.Errorf("failed to delete comment: %w", err)
	}
	return nil
}

// GetByID retrieves a comment by ID
func (r *CommentRepository) GetByID(id int64) (*models.Comment, error) {
	query := `SELECT id, post_id, author_id, content, created_at FROM comments WHERE id = ?`

	comment := &models.Comment{}
	err := r.db.QueryRow(query, id).Scan(
		&comment.ID,
		&comment.PostID,
		&comment.AuthorID,
		&comment.Content,
		&comment.CreatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get comment: %w", err)
	}

	return comment, nil
}
