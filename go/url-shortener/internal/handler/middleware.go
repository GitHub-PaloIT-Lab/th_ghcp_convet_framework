package handler

import (
	"context"
	"net/http"
)

// AuthMiddleware validates API key authentication
func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		apiKey := r.Header.Get("X-API-Key")

		if apiKey == "" {
			respondError(w, http.StatusUnauthorized, "Missing API key")
			return
		}

		// In a real application, validate the API key against a database
		// For this demo, we'll accept any non-empty key and use it as userID
		ctx := context.WithValue(r.Context(), "userID", apiKey)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
