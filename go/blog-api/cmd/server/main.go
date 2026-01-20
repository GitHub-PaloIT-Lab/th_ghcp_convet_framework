package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"github.com/yourusername/blog-api/internal/handler"
	"github.com/yourusername/blog-api/internal/middleware"
	"github.com/yourusername/blog-api/internal/repository"
	"github.com/yourusername/blog-api/internal/service"
)

func main() {
	// Initialize database
	db, err := repository.InitDB("./blog.db")
	if err != nil {
		log.Fatal("Failed to initialize database:", err)
	}
	defer db.Close()

	// Initialize repositories
	userRepo := repository.NewUserRepository(db)
	postRepo := repository.NewPostRepository(db)
	commentRepo := repository.NewCommentRepository(db)
	tagRepo := repository.NewTagRepository(db)

	// Initialize services
	authService := service.NewAuthService(userRepo)
	postService := service.NewPostService(postRepo, tagRepo)
	commentService := service.NewCommentService(commentRepo, postRepo)

	// Initialize handlers
	authHandler := handler.NewAuthHandler(authService)
	postHandler := handler.NewPostHandler(postService)
	commentHandler := handler.NewCommentHandler(commentService)
	tagHandler := handler.NewTagHandler(tagRepo)

	// Setup Gin router
	r := gin.Default()

	// CORS middleware
	r.Use(middleware.CORSMiddleware())

	// Public routes
	auth := r.Group("/api/auth")
	{
		auth.POST("/register", authHandler.Register)
		auth.POST("/login", authHandler.Login)
	}

	// Public posts (read-only)
	r.GET("/api/posts", postHandler.ListPosts)
	r.GET("/api/posts/:id", postHandler.GetPost)
	r.GET("/api/posts/search", postHandler.SearchPosts)
	r.GET("/api/tags", tagHandler.ListTags)

	// Protected routes
	api := r.Group("/api")
	api.Use(middleware.AuthMiddleware())
	{
		// Posts
		api.POST("/posts", postHandler.CreatePost)
		api.PUT("/posts/:id", postHandler.UpdatePost)
		api.DELETE("/posts/:id", postHandler.DeletePost)

		// Comments
		api.POST("/posts/:id/comments", commentHandler.CreateComment)
		api.DELETE("/comments/:id", commentHandler.DeleteComment)
	}

	// Start server
	log.Println("Server starting on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatal("Server failed:", err)
	}
}
