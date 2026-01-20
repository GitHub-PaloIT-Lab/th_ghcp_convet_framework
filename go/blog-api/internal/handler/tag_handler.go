package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/yourusername/blog-api/internal/repository"
)

// TagHandler handles tag HTTP requests
type TagHandler struct {
	tagRepo *repository.TagRepository
}

// NewTagHandler creates a new tag handler
func NewTagHandler(tagRepo *repository.TagRepository) *TagHandler {
	return &TagHandler{
		tagRepo: tagRepo,
	}
}

// ListTags handles GET /api/tags
func (h *TagHandler) ListTags(c *gin.Context) {
	tags, err := h.tagRepo.List()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, tags)
}
