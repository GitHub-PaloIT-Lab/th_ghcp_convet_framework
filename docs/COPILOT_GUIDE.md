# GitHub Copilot Guide for Cross-Language Conversion

## Overview

เอกสารนี้รวบรวม techniques, prompts และ best practices สำหรับการใช้ GitHub Copilot ในการแปลงโค้ดข้ามภาษาระหว่าง Go และ Python

---

## Table of Contents

1. [Getting Started with Copilot](#getting-started-with-copilot)
2. [Inline Suggestions Techniques](#inline-suggestions-techniques)
3. [Copilot Chat Strategies](#copilot-chat-strategies)
4. [Slash Commands](#slash-commands)
5. [Conversion Patterns](#conversion-patterns)
6. [Language-Specific Prompts](#language-specific-prompts)
7. [Common Pitfalls](#common-pitfalls)
8. [Advanced Techniques](#advanced-techniques)

---

## Getting Started with Copilot

### Basic Setup

1. **Enable Copilot** ใน VS Code
2. **Open Copilot Chat**: `Cmd+I` (Mac) or `Ctrl+I` (Windows/Linux)
3. **Toggle suggestions**: `Cmd+\` (Mac) or `Ctrl+\` (Windows/Linux)

### Best Practices

✅ **DO:**
- เขียน comments ที่ชัดเจนก่อนโค้ด
- ใช้ descriptive function/variable names
- แบ่งงานเป็นชิ้นเล็กๆ
- ทดสอบ suggestions ก่อน accept
- รีวิวโค้ดที่ Copilot generate

❌ **DON'T:**
- Accept ทุก suggestion โดยไม่อ่าน
- ปล่อยให้ Copilot เขียนโค้ดยาวๆ โดยไม่เข้าใจ
- Skip tests และ error handling
- ลืม refactor หลัง generate

---

## Inline Suggestions Techniques

### 1. Comment-Driven Development

**Technique**: เขียน comments อธิบายสิ่งที่ต้องการแล้ว Copilot จะ generate โค้ด

#### Example: Converting Go Struct to Pydantic Model

```python
# Convert the following Go struct to a Pydantic model:
# type URL struct {
#     ID          int64     `json:"id"`
#     ShortCode   string    `json:"short_code"`
#     OriginalURL string    `json:"original_url"`
#     UserID      string    `json:"user_id"`
#     CreatedAt   time.Time `json:"created_at"`
# }

from pydantic import BaseModel
from datetime import datetime

class URL(BaseModel):
    # Copilot will suggest the rest...
```

**Expected Result**:
```python
class URL(BaseModel):
    id: int
    short_code: str
    original_url: str
    user_id: str
    created_at: datetime
```

---

### 2. Function Signature First

**Technique**: เขียน function signature พร้อม docstring แล้วให้ Copilot implement

#### Example: Go Error Handling → Python Exceptions

```python
def create_short_url(self, original_url: str, user_id: str) -> URL:
    """
    Create a short URL from the original URL.
    
    Args:
        original_url: The original long URL
        user_id: The user ID who owns the URL
        
    Returns:
        URL: The created URL object
        
    Raises:
        ValueError: If original_url is invalid
        DatabaseError: If database operation fails
    """
    # Copilot will suggest implementation...
```

---

### 3. Type Hints for Better Suggestions

**Technique**: ใช้ type hints ให้ครบถ้วนเพื่อให้ Copilot เข้าใจ context

#### Example: Better Suggestions with Type Hints

```python
from typing import List, Optional, Protocol

class Cache(Protocol):
    """Cache interface matching Go's Cache interface"""
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        ...
    
    def set(self, key: str, value: str, expiration: int) -> None:
        """Set value in cache with expiration in seconds"""
        ...
    
    def delete(self, key: str) -> None:
        """Delete key from cache"""
        ...

# Copilot จะแนะนำ implementation ที่ถูกต้องมากขึ้น
class RedisCache:
    def __init__(self, host: str, port: int):
        # Implementation...
```

---

### 4. Progressive Building

**Technique**: สร้าง structure ก่อนแล้วค่อยๆ fill in details

#### Example: Building a Service Class

```python
# Step 1: Class structure
class URLService:
    def __init__(self, cache: Cache, store: Store):
        self.cache = cache
        self.store = store
    
    # Step 2: Method signatures (Copilot suggests)
    async def create_short_url(self, original_url: str, user_id: str) -> URL:
        pass
    
    # Step 3: Implement each method one by one
    async def create_short_url(self, original_url: str, user_id: str) -> URL:
        # Generate short code
        short_code = self._generate_short_code()
        # Copilot continues...
```

---

## Copilot Chat Strategies

### 1. Conversion Requests

**Best Prompts**:

```
Convert this Go struct to a Python Pydantic model with the same fields and validation:
[paste Go code]
```

```
Translate this Go function to Python, using async/await instead of goroutines:
[paste Go code]
```

```
Convert this Python class to a Go struct with methods:
[paste Python code]
```

---

### 2. Explaining Code

**Prompts**:

```
Explain what this Go function does and suggest equivalent Python approach:
[paste code]
```

```
What's the idiomatic Python way to implement this Go pattern?
[paste code]
```

---

### 3. Error Handling Conversion

**Prompts**:

```
Convert this Go error handling pattern to Python exceptions:
result, err := someFunction()
if err != nil {
    return nil, fmt.Errorf("failed: %w", err)
}
```

**Expected Response**:
```python
try:
    result = some_function()
except SomeError as e:
    raise RuntimeError(f"failed: {e}") from e
```

---

### 4. Dependency Mapping

**Prompts**:

```
What's the Python equivalent of Go's Chi router?
```

```
How do I replace Go's database/sql with Python? Should I use SQLAlchemy or raw sqlite3?
```

```
What Python library is similar to Go's goquery for web scraping?
```

---

## Slash Commands

### `/tests` - Generate Tests

**Usage**: เลือกโค้ดแล้วพิมพ์ `/tests` ใน Chat

**Example**:
```
/tests for the create_short_url function with edge cases
```

**What Copilot generates**:
- Happy path tests
- Error case tests
- Edge cases (empty strings, invalid input, etc.)
- Mock setup (if needed)

---

### `/doc` - Generate Documentation

**Usage**: เลือก function/class แล้วพิมพ์ `/doc`

**Example**:
```
/doc for the URLService class with detailed docstrings
```

**What Copilot generates**:
- Class docstring
- Method docstrings
- Parameter descriptions
- Return value descriptions
- Raises descriptions

---

### `/fix` - Fix Errors

**Usage**: เลือกโค้ดที่มี error แล้วพิมพ์ `/fix`

**Example**:
```
/fix the type hint errors in this function
```

**Useful for**:
- Type hint errors
- Import errors
- Syntax errors
- Logic bugs

---

### `/explain` - Explain Code

**Usage**: เลือกโค้ดแล้วพิมพ์ `/explain`

**Example**:
```
/explain how this pagination logic works
```

**Useful for**:
- Understanding complex code
- Learning new patterns
- Code review

---

## Conversion Patterns

### Pattern 1: Go Struct → Python Pydantic Model

**Prompt Template**:
```python
# Convert Go struct to Pydantic:
# [paste Go struct]

from pydantic import BaseModel, Field, validator
from datetime import datetime

class [ClassName](BaseModel):
    # Copilot suggests fields...
```

**Tips**:
- Copilot รู้จัก JSON tags และแปลงเป็น Field aliases
- Copilot จะเพิ่ม validators ถ้าเห็น validation logic ใน Go

---

### Pattern 2: Go Interface → Python Protocol/ABC

**Prompt Template**:
```python
# Implement Go interface in Python:
# type Cache interface {
#     Get(key string) (string, error)
#     Set(key string, value string, expiration time.Duration) error
# }

from typing import Protocol, Optional

class Cache(Protocol):
    # Copilot suggests methods...
```

---

### Pattern 3: Go Error Handling → Python Exceptions

**Before (Go)**:
```go
result, err := service.CreateURL(url)
if err != nil {
    return nil, fmt.Errorf("failed to create URL: %w", err)
}
```

**Prompt**:
```python
# Convert Go error handling to Python exceptions:
# [paste Go code]

try:
    # Copilot suggests...
```

**After (Python)**:
```python
try:
    result = service.create_url(url)
except ValueError as e:
    raise RuntimeError(f"failed to create URL: {e}") from e
```

---

### Pattern 4: Go Goroutines → Python Asyncio

**Before (Go)**:
```go
var wg sync.WaitGroup
results := make(chan WeatherData, len(sources))

for _, source := range sources {
    wg.Add(1)
    go func(s Source) {
        defer wg.Done()
        data, err := s.Fetch()
        if err == nil {
            results <- data
        }
    }(source)
}

wg.Wait()
close(results)
```

**Prompt**:
```python
# Convert Go goroutines to Python asyncio:
# [paste Go code]

import asyncio
from typing import List

async def fetch_all(sources: List[Source]) -> List[WeatherData]:
    # Copilot suggests...
```

**After (Python)**:
```python
async def fetch_all(sources: List[Source]) -> List[WeatherData]:
    tasks = [source.fetch() for source in sources]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]
```

---

### Pattern 5: Python Class → Go Struct with Methods

**Before (Python)**:
```python
class WeatherAggregator:
    def __init__(self, clients: List[APIClient], cache: Cache):
        self.clients = clients
        self.cache = cache
    
    async def get_weather(self, location: str) -> Weather:
        # implementation...
```

**Prompt in Chat**:
```
Convert this Python class to Go struct with methods, using goroutines instead of async/await
```

**After (Go)**:
```go
type WeatherAggregator struct {
    clients []APIClient
    cache   Cache
}

func NewWeatherAggregator(clients []APIClient, cache Cache) *WeatherAggregator {
    return &WeatherAggregator{
        clients: clients,
        cache:   cache,
    }
}

func (w *WeatherAggregator) GetWeather(ctx context.Context, location string) (*Weather, error) {
    // implementation with goroutines...
}
```

---

### Pattern 6: Table-Driven Tests Conversion

**Python (pytest with parametrize) → Go**:

**Prompt**:
```go
// Convert pytest parametrize to Go table-driven test:
// [paste Python test]

func TestCreateShortURL(t *testing.T) {
    tests := []struct {
        name string
        // Copilot suggests test cases...
```

**Go → Python**:

**Prompt**:
```python
# Convert Go table-driven test to pytest parametrize:
# [paste Go test]

import pytest

@pytest.mark.parametrize("test_input,expected", [
    # Copilot suggests test cases...
```

---

## Language-Specific Prompts

### Go → Python Conversions

#### 1. HTTP Handlers

**Prompt**:
```python
# Convert Chi HTTP handler to FastAPI:
# func (h *URLHandler) CreateShortURL(w http.ResponseWriter, r *http.Request) {
#     var req CreateURLRequest
#     json.NewDecoder(r.Body).Decode(&req)
#     // ...
# }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class CreateURLRequest(BaseModel):
    # Copilot suggests...

@router.post("/urls")
async def create_short_url(request: CreateURLRequest):
    # Copilot suggests...
```

---

#### 2. Database Operations

**Prompt**:
```python
# Convert Go database/sql to Python SQLAlchemy or raw sqlite3:
# row := db.QueryRow("SELECT * FROM urls WHERE short_code = ?", shortCode)
# var url URL
# err := row.Scan(&url.ID, &url.ShortCode, &url.OriginalURL)

import sqlite3
from typing import Optional

def get_url_by_code(self, short_code: str) -> Optional[URL]:
    # Copilot suggests...
```

---

#### 3. Middleware

**Prompt**:
```python
# Convert Go middleware to FastAPI middleware:
# func AuthMiddleware(next http.Handler) http.Handler {
#     return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
#         apiKey := r.Header.Get("X-API-Key")
#         if apiKey == "" {
#             w.WriteHeader(http.StatusUnauthorized)
#             return
#         }
#         next.ServeHTTP(w, r)
#     })
# }

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Copilot suggests...
```

---

### Python → Go Conversions

#### 1. Dataclasses/Pydantic → Structs

**Prompt**:
```go
// Convert Python dataclass to Go struct:
// @dataclass
// class WeatherData:
//     location: str
//     temperature: float
//     humidity: int
//     timestamp: datetime

type WeatherData struct {
    // Copilot suggests fields with JSON tags...
}
```

---

#### 2. Async/Await → Goroutines

**Prompt**:
```go
// Convert Python async function to Go with goroutines:
// async def fetch_all_weather(sources: List[Source]) -> List[Weather]:
//     tasks = [source.fetch() for source in sources]
//     return await asyncio.gather(*tasks)

func fetchAllWeather(sources []Source) ([]Weather, error) {
    // Copilot suggests goroutines with channels...
```

---

#### 3. Context Managers → Defer

**Prompt**:
```go
// Convert Python context manager to Go defer:
// with open("file.txt", "r") as f:
//     data = f.read()

func readFile(filename string) (string, error) {
    f, err := os.Open(filename)
    if err != nil {
        return "", err
    }
    defer f.Close() // Copilot suggests defer
    
    // Copilot continues...
}
```

---

#### 4. Decorators → Function Wrappers

**Prompt**:
```go
// Convert Python decorator to Go function wrapper:
// @retry(max_attempts=3)
// def fetch_data(url: str) -> str:
//     response = requests.get(url)
//     return response.text

func withRetry(maxAttempts int, fn func() (string, error)) (string, error) {
    // Copilot suggests retry logic...
}
```

---

## Common Pitfalls

### 1. Over-Accepting Suggestions

❌ **Problem**: Accept ทุก suggestion โดยไม่คิด

✅ **Solution**: 
- อ่านและเข้าใจก่อน accept
- ทดสอบว่าทำงานถูกต้อง
- ตรวจสอบว่าเป็น idiomatic code

---

### 2. Ignoring Type Safety

❌ **Problem**: ปล่อยให้ Python code ไม่มี type hints

✅ **Solution**:
```python
# Add type hints explicitly
def create_url(url: str, user_id: str) -> URL:  # ✅ Good
def create_url(url, user_id):  # ❌ Bad
```

---

### 3. Not Testing Converted Code

❌ **Problem**: แปลงเสร็จแล้วไม่ test

✅ **Solution**:
- ใช้ `/tests` generate tests ทันที
- Run tests หลังแปลงแต่ละ module
- เปรียบเทียบ behavior กับ original

---

### 4. Ignoring Error Handling

❌ **Problem**: Copilot อาจ skip error handling

✅ **Solution**:
```python
# Always add proper error handling
try:
    result = some_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

---

### 5. Not Reviewing Dependencies

❌ **Problem**: ใช้ dependencies ที่ Copilot แนะนำโดยไม่ตรวจสอบ

✅ **Solution**:
- ตรวจสอบว่า library ยังถูก maintain อยู่
- เช็ค version compatibility
- พิจารณา alternatives

---

## Advanced Techniques

### 1. Multi-Step Conversion

**Technique**: แบ่งการ convert เป็นหลายขั้นตอนแล้วให้ Copilot ช่วยทีละขั้น

**Example**:
```
Step 1: Convert just the data models
Step 2: Convert the interfaces/protocols
Step 3: Convert the business logic
Step 4: Convert the API layer
Step 5: Convert the tests
```

---

### 2. Context-Rich Comments

**Technique**: เพิ่ม context ให้มากเพื่อให้ Copilot เข้าใจดีขึ้น

**Example**:
```python
# This function converts a Go-style error return pattern to Python exceptions.
# In Go, we return (result, error), but in Python we raise exceptions.
# The original Go function signature was:
# func CreateURL(url string) (*URL, error)
# 
# Convert to Python async function that raises ValueError on invalid input
# and DatabaseError on database failures.

async def create_url(self, url: str) -> URL:
    # Copilot now has much better context...
```

---

### 3. Incremental Refactoring

**Technique**: Convert แล้ว refactor ทีละนิด

```python
# Step 1: Direct conversion (may not be idiomatic)
def create_url(self, url: str) -> tuple[URL, Exception]:
    # Direct Go-to-Python translation
    pass

# Step 2: Ask Copilot to make it idiomatic
# "Refactor this function to be more Pythonic with exceptions"

# Step 3: Final idiomatic version
async def create_url(self, url: str) -> URL:
    # Idiomatic Python with exceptions
    pass
```

---

### 4. Batch Conversion with Chat

**Technique**: ใช้ Chat แปลงหลายๆ functions พร้อมกัน

**Prompt**:
```
Convert these 5 Go methods to Python:
1. CreateURL
2. GetURL
3. DeleteURL
4. ListURLs
5. UpdateURL

Maintain the same logic but use Python idioms, async/await, and exceptions.
```

---

### 5. Learning Mode

**Technique**: ใช้ Copilot เป็น teacher

**Prompts**:
```
Explain the differences between Go interfaces and Python Protocols

Show me 3 ways to implement this pattern in Python

What are the pros and cons of each approach?

Which is most idiomatic?
```

---

## Conversion Workflow with Copilot

### Recommended Flow:

1. **Read Original Code** (5 min)
   - เข้าใจ logic ก่อน

2. **Setup Structure** (10 min)
   ```python
   # Create file structure
   # Add imports
   # Define models/classes
   ```

3. **Convert Models** (15 min)
   - ใช้ comment-driven development
   - Copilot suggests conversions

4. **Convert Logic** (30-60 min)
   - ทีละ function/method
   - Test after each conversion

5. **Add Error Handling** (15 min)
   ```python
   # Ask Copilot: "Add proper error handling"
   ```

6. **Generate Tests** (20 min)
   ```
   /tests for all functions with edge cases
   ```

7. **Generate Docs** (10 min)
   ```
   /doc for all classes and functions
   ```

8. **Final Review** (10 min)
   - Run all tests
   - Check for TODO comments
   - Verify idiomatic code

---

## Quick Reference

### Most Useful Prompts

| Task | Prompt |
|------|--------|
| Convert struct | `Convert this Go struct to Python Pydantic model` |
| Convert function | `Translate this function to [target language], maintaining the same logic` |
| Error handling | `Convert this error handling to Python exceptions` |
| Tests | `/tests with edge cases and mocks` |
| Documentation | `/doc with detailed docstrings` |
| Fix errors | `/fix type hint errors` |
| Explain | `/explain how this works` |
| Refactor | `Make this code more idiomatic in [language]` |
| Dependencies | `What's the [language] equivalent of [library]?` |

---

### Keyboard Shortcuts

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Accept suggestion | `Tab` | `Tab` |
| Reject suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Alt+]` |
| Previous suggestion | `Alt+[` | `Alt+[` |
| Open Chat | `Cmd+I` | `Ctrl+I` |
| Toggle Copilot | `Cmd+\` | `Ctrl+\` |

---

## Success Tips

1. ✅ **Start Small**: Convert ทีละ module แทนทั้งแอพ
2. ✅ **Test Often**: Run tests หลัง convert แต่ละส่วน
3. ✅ **Read Suggestions**: อย่า blind accept
4. ✅ **Add Context**: เขียน comments ให้ Copilot เข้าใจ
5. ✅ **Use Chat**: ถามเมื่อไม่แน่ใจ
6. ✅ **Iterate**: Refactor หลังได้ working version
7. ✅ **Learn**: ใช้โอกาสนี้เรียนรู้ idioms ของภาษา
8. ✅ **Document**: Generate docs ด้วย `/doc`

Good luck with your conversions! 🚀
