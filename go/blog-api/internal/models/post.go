package models

import "time"

// Post represents a blog post
type Post struct {
	ID        int64     `json:"id"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	AuthorID  int64     `json:"author_id"`
	Author    *User     `json:"author,omitempty"`
	Tags      []Tag     `json:"tags,omitempty"`
	Comments  []Comment `json:"comments,omitempty"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// CreatePostRequest is the request for creating a post
type CreatePostRequest struct {
	Title   string   `json:"title" binding:"required,min=1,max=200"`
	Content string   `json:"content" binding:"required,min=1"`
	Tags    []string `json:"tags"`
}

// UpdatePostRequest is the request for updating a post
type UpdatePostRequest struct {
	Title   string   `json:"title" binding:"required,min=1,max=200"`
	Content string   `json:"content" binding:"required,min=1"`
	Tags    []string `json:"tags"`
}
