package main

import (
	"log"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/yourusername/url-shortener/internal/handler"
	"github.com/yourusername/url-shortener/internal/service"
	"github.com/yourusername/url-shortener/internal/storage"
)

func main() {
	// Initialize storage
	store, err := storage.NewSQLiteStore("./urls.db")
	if err != nil {
		log.Fatal("Failed to initialize database:", err)
	}
	defer store.Close()

	// Initialize SQLite cache (same database)
	cache, err := storage.NewSQLiteCache(store.DB())
	if err != nil {
		log.Fatal("Failed to initialize cache:", err)
	}

	// Initialize service
	urlService := service.NewURLService(cache, store)
	analyticsService := service.NewAnalyticsService(store)

	// Initialize handlers
	urlHandler := handler.NewURLHandler(urlService)
	analyticsHandler := handler.NewAnalyticsHandler(analyticsService)

	// Setup router
	r := chi.NewRouter()

	// Middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.RequestID)

	// Routes
	r.Route("/api", func(r chi.Router) {
		r.Use(handler.AuthMiddleware)
		r.Post("/urls", urlHandler.CreateShortURL)
		r.Get("/urls", urlHandler.ListURLs)
		r.Delete("/urls/{shortCode}", urlHandler.DeleteURL)
		r.Get("/analytics/{shortCode}", analyticsHandler.GetAnalytics)
	})

	// Public redirect route
	r.Get("/{shortCode}", urlHandler.RedirectURL)

	// Start server
	port := getEnv("PORT", "8080")
	log.Printf("Server starting on port %s", port)
	if err := http.ListenAndServe(":"+port, r); err != nil {
		log.Fatal("Server failed:", err)
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
