package models

import "time"

// Comment represents a comment on a post
type Comment struct {
	ID        int64     `json:"id"`
	PostID    int64     `json:"post_id"`
	AuthorID  int64     `json:"author_id"`
	Author    *User     `json:"author,omitempty"`
	Content   string    `json:"content"`
	CreatedAt time.Time `json:"created_at"`
}

// CreateCommentRequest is the request for creating a comment
type CreateCommentRequest struct {
	Content string `json:"content" binding:"required,min=1"`
}
