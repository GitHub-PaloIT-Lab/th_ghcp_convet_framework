# GitHub Copilot Instructions - Convert Framework Workshop

## Overview
This project is a workshop demonstrating cross-language code conversion between Go and Python using GitHub Copilot. The goal is to help developers migrate applications between languages efficiently while maintaining code quality and idiomatic patterns.

## Cross-Language Conversion Best Practices

### Go → Python Conversion

**Type System Mapping:**
- Go structs → Python dataclasses or Pydantic models
- Go interfaces → Python Protocols or Abstract Base Classes
- Go pointers → Python objects (no pointer equivalent needed)
- Go channels → Python queues (queue.Queue or asyncio.Queue)
- Go slices → Python lists
- Go maps → Python dictionaries

**Idiom Translation:**
- Go error returns → Python exceptions with try/except
- Go goroutines → Python asyncio tasks or threading
- Go defer → Python context managers or try/finally
- Go multiple return values → Python tuples or named tuples
- Go method receivers → Python class methods with self

**Naming Conventions:**
- Go PascalCase (exported) → Python snake_case
- Go camelCase (unexported) → Python snake_case with _ prefix
- Go constants SCREAMING_SNAKE_CASE → Python SCREAMING_SNAKE_CASE

**Code Style:**
- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Use docstrings (Google or NumPy style)
- Prefer list comprehensions over loops when readable
- Use f-strings for string formatting

### Python → Go Conversion

**Type System Mapping:**
- Python classes → Go structs with methods
- Python dataclasses → Go structs
- Python Protocols → Go interfaces
- Python lists → Go slices
- Python dicts → Go maps
- Python None → Go nil or zero values

**Idiom Translation:**
- Python exceptions → Go error returns
- Python async/await → Go goroutines and channels
- Python context managers → Go defer
- Python decorators → Go function wrappers or middleware
- Python generators → Go channels or iterators

**Naming Conventions:**
- Python snake_case → Go camelCase (unexported) or PascalCase (exported)
- Python _private → Go unexported (lowercase first letter)
- Python CONSTANTS → Go const with PascalCase

**Code Style:**
- Follow effective Go guidelines
- Use early returns for error handling
- Keep functions small and focused
- Use interfaces for abstraction
- Prefer explicit over implicit
- Handle all errors explicitly

## Error Handling Patterns

### Go Error Handling
```go
result, err := someFunction()
if err != nil {
    return nil, fmt.Errorf("failed to do something: %w", err)
}
```

### Python Exception Handling
```python
try:
    result = some_function()
except SomeError as e:
    raise RuntimeError(f"Failed to do something: {e}") from e
```

## Concurrency Patterns

### Go Concurrency
- Use goroutines for concurrent operations
- Use channels for communication
- Use sync.WaitGroup for coordinating goroutines
- Use context.Context for cancellation

### Python Concurrency
- Use asyncio for I/O-bound operations
- Use threading for I/O-bound with sync libraries
- Use multiprocessing for CPU-bound operations
- Prefer async/await patterns for modern code

## Testing Patterns

### Go Tests
- Use testing package
- Table-driven tests preferred
- Test file naming: `*_test.go`
- Function naming: `TestFunctionName`

### Python Tests
- Use pytest framework
- Fixtures for setup/teardown
- Test file naming: `test_*.py`
- Function naming: `test_function_name`

## Dependency Management

### Go Dependencies
- Use go.mod for dependency management
- Prefer standard library when possible
- Common packages: gin, chi, sqlx, testify

### Python Dependencies
- Use pyproject.toml or requirements.txt
- Use virtual environments
- Common packages: fastapi, flask, requests, pytest

## Configuration Management

### Go Configuration
- Use environment variables via os.Getenv
- Use viper or envconfig for complex configs
- Type-safe configuration structs

### Python Configuration
- Use python-dotenv for .env files
- Use pydantic-settings for validation
- Type-safe configuration with dataclasses

## Code Generation Guidelines

When generating code for conversion:

1. **Preserve Business Logic**: Keep the core functionality identical
2. **Use Idiomatic Patterns**: Write code that feels natural in the target language
3. **Maintain Test Coverage**: Convert tests along with implementation
4. **Document Changes**: Add comments explaining non-obvious conversions
5. **Handle Dependencies**: Find equivalent libraries in target language
6. **Validate Types**: Ensure type safety in both languages
7. **Consider Performance**: Be aware of performance differences between languages
8. **Keep It Simple**: Don't over-engineer the conversion

## Workshop-Specific Guidelines

- Write clear, educational code suitable for learning
- Add comments explaining language-specific features
- Include TODO comments for workshop participants
- Keep functions focused and easy to understand
- Provide both simple and advanced examples
- Include error handling best practices
- Write comprehensive tests that demonstrate usage
