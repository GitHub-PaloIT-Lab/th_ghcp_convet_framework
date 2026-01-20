package service

import (
	"fmt"

	"github.com/yourusername/blog-api/internal/models"
	"github.com/yourusername/blog-api/internal/repository"
)

// PostService handles post business logic
type PostService struct {
	postRepo *repository.PostRepository
	tagRepo  *repository.TagRepository
}

// NewPostService creates a new post service
func NewPostService(postRepo *repository.PostRepository, tagRepo *repository.TagRepository) *PostService {
	return &PostService{
		postRepo: postRepo,
		tagRepo:  tagRepo,
	}
}

// CreatePost creates a new post with tags
func (s *PostService) CreatePost(req *models.CreatePostRequest, authorID int64) (*models.Post, error) {
	// Create post
	post := &models.Post{
		Title:    req.Title,
		Content:  req.Content,
		AuthorID: authorID,
	}

	if err := s.postRepo.Create(post); err != nil {
		return nil, fmt.Errorf("failed to create post: %w", err)
	}

	// Handle tags
	if len(req.Tags) > 0 {
		tagIDs, err := s.getOrCreateTags(req.Tags)
		if err != nil {
			return nil, fmt.Errorf("failed to handle tags: %w", err)
		}

		if err := s.postRepo.AddTags(post.ID, tagIDs); err != nil {
			return nil, fmt.Errorf("failed to add tags: %w", err)
		}
	}

	// Get the complete post with author and tags
	return s.GetPostByID(post.ID)
}

// GetPostByID retrieves a post with its author, tags, and comments
func (s *PostService) GetPostByID(id int64) (*models.Post, error) {
	post, err := s.postRepo.GetByID(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get post: %w", err)
	}
	if post == nil {
		return nil, fmt.Errorf("post not found")
	}

	// Get tags
	tags, err := s.postRepo.GetPostTags(id)
	if err != nil {
		return nil, err
	}
	post.Tags = tags

	return post, nil
}

// ListPosts retrieves posts with pagination
func (s *PostService) ListPosts(limit, offset int) ([]*models.Post, error) {
	posts, err := s.postRepo.List(limit, offset)
	if err != nil {
		return nil, fmt.Errorf("failed to list posts: %w", err)
	}

	// Load tags for each post
	for _, post := range posts {
		tags, err := s.postRepo.GetPostTags(post.ID)
		if err != nil {
			return nil, err
		}
		post.Tags = tags
	}

	return posts, nil
}

// UpdatePost updates a post
func (s *PostService) UpdatePost(id int64, req *models.UpdatePostRequest, userID int64) error {
	// Get existing post
	post, err := s.postRepo.GetByID(id)
	if err != nil {
		return fmt.Errorf("failed to get post: %w", err)
	}
	if post == nil {
		return fmt.Errorf("post not found")
	}

	// Check authorization
	if post.AuthorID != userID {
		return fmt.Errorf("unauthorized: you can only edit your own posts")
	}

	// Update post
	post.Title = req.Title
	post.Content = req.Content

	if err := s.postRepo.Update(post); err != nil {
		return fmt.Errorf("failed to update post: %w", err)
	}

	// Update tags
	if len(req.Tags) > 0 {
		tagIDs, err := s.getOrCreateTags(req.Tags)
		if err != nil {
			return fmt.Errorf("failed to handle tags: %w", err)
		}

		if err := s.postRepo.AddTags(post.ID, tagIDs); err != nil {
			return fmt.Errorf("failed to update tags: %w", err)
		}
	}

	return nil
}

// DeletePost deletes a post
func (s *PostService) DeletePost(id int64, userID int64) error {
	// Get existing post
	post, err := s.postRepo.GetByID(id)
	if err != nil {
		return fmt.Errorf("failed to get post: %w", err)
	}
	if post == nil {
		return fmt.Errorf("post not found")
	}

	// Check authorization
	if post.AuthorID != userID {
		return fmt.Errorf("unauthorized: you can only delete your own posts")
	}

	return s.postRepo.Delete(id)
}

// SearchPosts searches for posts by title or content
func (s *PostService) SearchPosts(query string) ([]*models.Post, error) {
	posts, err := s.postRepo.Search(query)
	if err != nil {
		return nil, fmt.Errorf("failed to search posts: %w", err)
	}

	// Load tags for each post
	for _, post := range posts {
		tags, err := s.postRepo.GetPostTags(post.ID)
		if err != nil {
			return nil, err
		}
		post.Tags = tags
	}

	return posts, nil
}

// getOrCreateTags gets existing tags or creates new ones
func (s *PostService) getOrCreateTags(tagNames []string) ([]int64, error) {
	tagIDs := make([]int64, 0, len(tagNames))

	for _, name := range tagNames {
		tag, err := s.tagRepo.GetOrCreate(name)
		if err != nil {
			return nil, err
		}
		tagIDs = append(tagIDs, tag.ID)
	}

	return tagIDs, nil
}
