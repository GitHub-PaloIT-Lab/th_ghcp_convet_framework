# Blog REST API

A RESTful API for a blog platform with posts, comments, tags, and JWT authentication, built with Go, Gin framework, and SQLite database.

## ⚡ Quick Run

```bash
# 1. Install dependencies
go mod download

# 2. Run the server
go run cmd/server/main.go
# → Server starts at http://localhost:8080
```

## 🧪 Test It

```bash
# 1. Register a user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Response: {"token":"eyJhbGc..."}

# 2. Create a post (save the token from above)
TOKEN="your-jwt-token-here"
curl -X POST http://localhost:8080/api/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Post","content":"Hello World!","tags":["intro","test"]}'

# 3. Get all posts
curl http://localhost:8080/api/posts

# 4. Add a comment
curl -X POST http://localhost:8080/api/posts/1/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Great post!"}'
```

## Features

- ✅ User registration and JWT authentication
- ✅ Create, read, update, delete blog posts
- ✅ Add comments to posts  
- ✅ Tag posts with multiple tags
- ✅ Filter and search posts
- ✅ User authorization (only owner can edit/delete)
- ✅ RESTful API design

## Tech Stack

- **Go 1.21+**
- **Gin** - HTTP framework
- **SQLite** - Database
- **JWT** - Authentication
- **bcrypt** - Password hashing

## Project Structure

```
blog-api/
├── cmd/
│   └── server/
│       └── main.go              # Entry point
├── internal/
│   ├── handler/
│   │   ├── auth_handler.go      # Authentication handlers
│   │   ├── post_handler.go      # Post handlers
│   │   ├── comment_handler.go   # Comment handlers
│   │   └── tag_handler.go       # Tag handlers
│   ├── service/
│   │   ├── auth_service.go      # Auth business logic
│   │   ├── post_service.go      # Post business logic
│   │   └── comment_service.go   # Comment business logic
│   ├── repository/
│   │   ├── db.go                # Database initialization
│   │   ├── user_repository.go   # User database operations
│   │   ├── post_repository.go   # Post database operations
│   │   ├── comment_repository.go
│   │   └── tag_repository.go
│   ├── middleware/
│   │   ├── auth.go              # JWT middleware
│   │   └── cors.go              # CORS middleware
│   ├── models/
│   │   ├── user.go              # User models
│   │   ├── post.go              # Post models
│   │   ├── comment.go           # Comment models
│   │   └── tag.go               # Tag models
│   └── utils/
│       └── password.go          # Password hashing utilities
├── go.mod
├── go.sum
└── README.md
```

## Installation

1. **Install dependencies**
   ```bash
   cd go/blog-api
   go mod download
   ```

2. **Run the server**
   ```bash
   go run cmd/server/main.go
   ```

   The server will start on `http://localhost:8080`

## API Endpoints

### Authentication

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "created_at": "2026-01-20T10:30:00Z"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

### Posts

#### Create Post (Authenticated)
```http
POST /api/posts
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "This is the content of my post...",
  "tags": ["golang", "web-development"]
}
```

#### List Posts
```http
GET /api/posts?limit=20&offset=0
```

#### Get Single Post
```http
GET /api/posts/1
```

**Response**:
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content...",
  "author_id": 1,
  "author": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  "tags": [
    {"id": 1, "name": "golang"},
    {"id": 2, "name": "web-development"}
  ],
  "created_at": "2026-01-20T10:30:00Z",
  "updated_at": "2026-01-20T10:30:00Z"
}
```

#### Update Post (Authenticated, Owner Only)
```http
PUT /api/posts/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content...",
  "tags": ["golang"]
}
```

#### Delete Post (Authenticated, Owner Only)
```http
DELETE /api/posts/1
Authorization: Bearer <token>
```

#### Search Posts
```http
GET /api/posts/search?q=golang
```

### Comments

#### Add Comment (Authenticated)
```http
POST /api/posts/1/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Great post!"
}
```

#### Delete Comment (Authenticated, Owner Only)
```http
DELETE /api/comments/1
Authorization: Bearer <token>
```

### Tags

#### List All Tags
```http
GET /api/tags
```

## Example Usage

```bash
# Register a new user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Create a post (use token from login)
curl -X POST http://localhost:8080/api/posts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Content here","tags":["golang"]}'

# List posts
curl http://localhost:8080/api/posts

# Get a specific post
curl http://localhost:8080/api/posts/1

# Search posts
curl "http://localhost:8080/api/posts/search?q=golang"

# Add a comment
curl -X POST http://localhost:8080/api/posts/1/comments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Great post!"}'
```

## Conversion Target

This application is designed to be converted to **Python with Django REST Framework**.

### Key Conversion Points:

1. **Gin framework → Django REST Framework**
   - HTTP handlers → DRF ViewSets/APIViews
   - Routing → Django URL patterns
   - Middleware → Django middleware/DRF permissions

2. **Repository pattern → Django ORM**
   - Manual SQL → ORM queries
   - Explicit transactions → Django's transaction management

3. **JWT authentication → djangorestframework-simplejwt**
   - Custom JWT handling → DRF's built-in JWT

4. **Go structs → Django models & serializers**
   - Manual validation → DRF serializers
   - Type safety → Python type hints

5. **Error handling**
   - Go error returns → Python exceptions
   - Custom error responses → DRF exception handlers

## Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);
```

## Security Notes

⚠️ **This is a workshop example. For production:**
- Change JWT secret key (use environment variable)
- Add rate limiting
- Add input sanitization
- Use HTTPS
- Add proper logging
- Implement refresh tokens
- Add password complexity requirements

## License

This is a workshop example application.
