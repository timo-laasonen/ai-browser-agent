# Migration Guide - Updated API

## Summary of Changes

The AI Browser Agent has been improved with the following critical fixes:

### 1. ✅ AsyncOpenAI Implementation
- Replaced synchronous `OpenAI` client with `AsyncOpenAI`
- All LLM API calls now properly use `await` for non-blocking operations
- Improves performance in async contexts

### 2. ✅ Comprehensive Logging
- Added structured logging throughout all modules
- Logs include timestamps, module names, and severity levels
- Better debugging and production monitoring

### 3. ✅ Proper Token Counting
- Integrated `tiktoken` library for accurate token counting
- HTML truncation now preserves structure by using proper token-based truncation
- Fallback mechanism if tiktoken fails

### 4. ✅ Generic LLMProcessor
- `LLMProcessor` now accepts any Pydantic model via type parameter
- No longer hardcoded to `DeeplearningCourseList`
- Can be reused for any web scraping task

### 5. ✅ Improved Error Handling
- Exceptions are properly logged with stack traces
- Errors are re-raised for proper handling by calling code
- Added detailed error messages for better debugging

## API Changes

### Before
```python
# Old API - hardcoded model
service = ScrapingService()
result, screenshot = await service.scrape_and_process(
    TARGET_URL, 
    DEFAULT_INSTRUCTIONS
)
```

### After
```python
# New API - pass the model class as a parameter
from models import DeeplearningCourseList

service = ScrapingService()
result, screenshot = await service.scrape_and_process(
    TARGET_URL, 
    DEFAULT_INSTRUCTIONS,
    DeeplearningCourseList  # Specify the response model
)
```

## Using with Custom Models

You can now use the scraper with any Pydantic model:

```python
from pydantic import BaseModel
from typing import List

# Define your custom model
class Product(BaseModel):
    name: str
    price: float
    description: str
    image_url: str

class ProductList(BaseModel):
    products: List[Product]

# Use it with the scraper
service = ScrapingService()
result, screenshot = await service.scrape_and_process(
    "https://example.com/products",
    "Extract all product information including name, price, description, and image URL",
    ProductList  # Use your custom model
)

# result will be type ProductList with proper type hints
for product in result.products:
    print(f"{product.name}: ${product.price}")
```

## Logging Configuration

Logging is configured in `config.py`. You can adjust the level:

```python
# In config.py
LOG_LEVEL = logging.DEBUG  # For more verbose output
LOG_LEVEL = logging.INFO   # Default - balanced
LOG_LEVEL = logging.WARNING  # Less verbose
LOG_LEVEL = logging.ERROR  # Only errors
```

## New Dependencies

Install the new dependency:

```bash
pip install tiktoken==0.8.0
```

Or reinstall all dependencies:

```bash
pip install -r requirements.txt
```

## Error Handling Best Practices

The new code properly raises exceptions. Handle them appropriately:

```python
try:
    result, screenshot = await service.scrape_and_process(
        url, instructions, MyModel
    )
    # Process successful result
except ValueError as e:
    # Handle configuration errors (missing API key, etc.)
    logger.error(f"Configuration error: {e}")
except Exception as e:
    # Handle scraping/processing errors
    logger.error(f"Scraping failed: {e}")
```

## Breaking Changes

1. **`scrape_and_process()` signature changed** - now requires `response_model` parameter
2. **Exceptions are now raised** - calling code should handle exceptions instead of just checking for None
3. **`webscraper()` function signature changed** - now requires `response_model` parameter

## Benefits

- **Performance**: True async operations, no blocking
- **Reliability**: Proper error handling and logging
- **Flexibility**: Works with any Pydantic model
- **Accuracy**: Correct token counting prevents truncation issues
- **Maintainability**: Better logging makes debugging easier
