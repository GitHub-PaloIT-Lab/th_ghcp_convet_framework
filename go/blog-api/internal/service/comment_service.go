package service

import (
	"fmt"

	"github.com/yourusername/blog-api/internal/models"
	"github.com/yourusername/blog-api/internal/repository"
)

// CommentService handles comment business logic
type CommentService struct {
	commentRepo *repository.CommentRepository
	postRepo    *repository.PostRepository
}

// NewCommentService creates a new comment service
func NewCommentService(commentRepo *repository.CommentRepository, postRepo *repository.PostRepository) *CommentService {
	return &CommentService{
		commentRepo: commentRepo,
		postRepo:    postRepo,
	}
}

// CreateComment creates a new comment on a post
func (s *CommentService) CreateComment(postID int64, req *models.CreateCommentRequest, authorID int64) (*models.Comment, error) {
	// Verify post exists
	post, err := s.postRepo.GetByID(postID)
	if err != nil {
		return nil, fmt.Errorf("failed to get post: %w", err)
	}
	if post == nil {
		return nil, fmt.Errorf("post not found")
	}

	// Create comment
	comment := &models.Comment{
		PostID:   postID,
		AuthorID: authorID,
		Content:  req.Content,
	}

	if err := s.commentRepo.Create(comment); err != nil {
		return nil, fmt.Errorf("failed to create comment: %w", err)
	}

	return comment, nil
}

// DeleteComment deletes a comment
func (s *CommentService) DeleteComment(id int64, userID int64) error {
	// Get existing comment
	comment, err := s.commentRepo.GetByID(id)
	if err != nil {
		return fmt.Errorf("failed to get comment: %w", err)
	}
	if comment == nil {
		return fmt.Errorf("comment not found")
	}

	// Check authorization
	if comment.AuthorID != userID {
		return fmt.Errorf("unauthorized: you can only delete your own comments")
	}

	return s.commentRepo.Delete(id)
}

// GetPostComments retrieves all comments for a post
func (s *CommentService) GetPostComments(postID int64) ([]models.Comment, error) {
	return s.commentRepo.GetByPostID(postID)
}
