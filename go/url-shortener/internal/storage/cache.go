package storage

import (
	"context"
	"time"

	"github.com/go-redis/redis/v8"
)

// Cache defines the interface for caching operations
type Cache interface {
	Get(key string) (string, error)
	Set(key string, value string, expiration time.Duration) error
	Delete(key string) error
}

// RedisCache implements the Cache interface using Redis
type RedisCache struct {
	client *redis.Client
	ctx    context.Context
}

// NewRedisCache creates a new Redis cache instance
func NewRedisCache(addr string) *RedisCache {
	client := redis.NewClient(&redis.Options{
		Addr: addr,
	})

	return &RedisCache{
		client: client,
		ctx:    context.Background(),
	}
}

// Get retrieves a value from the cache
func (c *RedisCache) Get(key string) (string, error) {
	val, err := c.client.Get(c.ctx, key).Result()
	if err == redis.Nil {
		return "", nil // Key does not exist
	}
	return val, err
}

// Set stores a value in the cache with expiration
func (c *RedisCache) Set(key string, value string, expiration time.Duration) error {
	return c.client.Set(c.ctx, key, value, expiration).Err()
}

// Delete removes a key from the cache
func (c *RedisCache) Delete(key string) error {
	return c.client.Del(c.ctx, key).Err()
}
