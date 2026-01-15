# AI Browser Agent - Copilot Instructions

## Project Overview
This is a Python web scraping application that combines Playwright browser automation with OpenAI LLM processing to extract structured data from web pages. The system scrapes web content, processes HTML with AI, and returns strongly-typed Pydantic models.

## Architecture Principles

### Modular Design
- Each component has a single responsibility
- Clear separation between scraping, processing, and orchestration
- Use dependency injection where appropriate
- Always use async/await for I/O operations

### Code Organization
```
src/
├── models.py           # Pydantic data models (define schemas)
├── web_scraper.py      # Browser automation (Playwright)
├── llm_processor.py    # LLM processing (OpenAI structured output)
├── scraping_service.py # Orchestration layer
├── config.py           # Centralized configuration
├── helpers.py          # Utility functions
└── main.py             # Entry point
```

## Coding Standards

### Python Best Practices
- Use Python 3.8+ features (type hints, async/await, dataclasses)
- Follow PEP 8 style guide
- Use meaningful variable names (descriptive, not abbreviated)
- Add docstrings to all classes and functions
- Use f-strings for string formatting
- Prefer composition over inheritance

### Type Annotations
```python
# Always include type hints
async def scrape_content(self, url: str) -> str:
    """Scrape content from URL."""
    pass

# Use typing module for complex types
from typing import List, Optional, Tuple
```

### Error Handling
- Use try/except blocks for external operations (API calls, web scraping)
- Provide meaningful error messages with context
- Log errors with appropriate severity levels
- Clean up resources in finally blocks or use context managers

```python
async with WebScraperAgent() as scraper:
    try:
        html = await scraper.scrape_content(url)
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")
```

## Component-Specific Guidelines

### Pydantic Models (models.py)
- Use Pydantic BaseModel for all data structures
- Add field descriptions and validators where appropriate
- Keep models simple and focused
- Use List[], Optional[], and other typing generics
- Model names should be descriptive nouns (e.g., `DeeplearningCourse`)

```python
from pydantic import BaseModel, Field
from typing import List

class Course(BaseModel):
    """Represents a course with metadata."""
    title: str = Field(..., description="Course title")
    description: str
    presenters: List[str]
```

### Web Scraping (web_scraper.py)
- Use Playwright's async API exclusively
- Implement context managers for proper cleanup
- Configure browser with appropriate args from config
- Always handle timeouts gracefully
- Take screenshots for debugging/visualization
- Wait for content to load before scraping

```python
async with async_playwright() as p:
    browser = await p.chromium.launch(args=BROWSER_ARGS)
    page = await browser.new_page()
    await page.goto(url, wait_until="networkidle")
```

### LLM Processing (llm_processor.py)
- Use OpenAI's structured output with Pydantic schemas
- Truncate HTML to stay within token limits
- Set temperature low (0.1) for consistent extraction
- Handle API errors and rate limits
- Return strongly-typed models, not raw JSON
- Add clear instructions to the LLM prompt

```python
completion = await client.beta.chat.completions.parse(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    response_format=CourseList,
    temperature=0.1
)
```

### Configuration (config.py)
- Centralize all constants and settings
- Use environment variables for sensitive data (API keys)
- Group related settings together
- Use UPPER_CASE for constants
- Add comments explaining non-obvious settings

### Service Layer (scraping_service.py)
- Orchestrate between scraper and processor
- Keep business logic in services
- Return results and artifacts together (data + screenshots)
- Handle high-level error scenarios
- Provide clean async interfaces

## Async/Await Patterns

### Always Use Async for I/O
- Network requests (Playwright, OpenAI API)
- File operations when possible
- Any operation that waits for external resources

### Proper Async Context
```python
# Main entry point
if __name__ == "__main__":
    asyncio.run(main())

# In async functions
result = await some_async_function()

# Multiple async operations
results = await asyncio.gather(task1(), task2())
```

## Testing Guidelines

### Test Structure
- Place tests in `tests/` directory
- Name test files with `test_` prefix
- Use pytest for async testing
- Mock external dependencies (API calls, browser)

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_scrape_content():
    with patch('playwright.async_api.async_playwright'):
        # Test implementation
        pass
```

## Dependencies Management

### Key Dependencies
- **playwright**: Browser automation
- **openai**: LLM API with structured outputs
- **pydantic**: Data validation and serialization
- **pandas**: Data manipulation
- **python-dotenv**: Environment variable management

### Adding New Dependencies
1. Add to `requirements.txt` with version pinning
2. Update README.md if it's a major dependency
3. Consider if it could be optional

## Common Patterns

### Context Managers for Resources
```python
async with WebScraperAgent() as scraper:
    content = await scraper.scrape_content(url)
    # Browser automatically closed
```

### Configuration Access
```python
from config import TARGET_URL, DEFAULT_MODEL, BROWSER_ARGS
# Use constants instead of hardcoding values
```

### Structured Data Extraction
```python
# Define schema
class DataModel(BaseModel):
    field: str

# Extract with LLM
result = await processor.process_html_to_structured_data(
    html, instructions, DataModel
)
```

## Performance Considerations

- Keep HTML truncation reasonable (150k tokens max)
- Use browser args to disable unnecessary features
- Close browser contexts properly
- Consider rate limits for API calls
- Cache results when appropriate

## Security Best Practices

- Never commit API keys (use environment variables)
- Use `python-dotenv` for local development
- Validate all external inputs
- Be cautious with eval() or exec()
- Use browser security flags appropriately

## Documentation Standards

### Function Docstrings
```python
async def scrape_content(self, url: str) -> str:
    """
    Scrape HTML content from a URL using Playwright.
    
    Args:
        url: The target URL to scrape
        
    Returns:
        str: The HTML content of the page
        
    Raises:
        PlaywrightError: If navigation fails
    """
```

### Module Docstrings
```python
"""
Module for web scraping functionality using Playwright.

This module provides the WebScraperAgent class for browser automation
and HTML content extraction.
"""
```

## When Adding New Features

1. **Define data model first** (in models.py if needed)
2. **Update config** for new constants/settings
3. **Implement core logic** in appropriate module
4. **Add to service layer** for orchestration
5. **Update main.py** for new entry points
6. **Write tests** for new functionality
7. **Update README** if user-facing

## Common Tasks

### Adding a New Data Model
1. Define in `models.py` with Pydantic
2. Add type hints and descriptions
3. Use in LLM processor's structured output
4. Update relevant functions to return the model

### Scraping a New Website
1. Add URL to `config.py`
2. Define Pydantic model for expected data structure
3. Create extraction instructions
4. Test with different pages
5. Handle edge cases (missing data, timeouts)

### Modifying Browser Behavior
1. Update `BROWSER_ARGS` in `config.py`
2. Test that scraping still works
3. Consider performance impact
4. Document any browser-specific quirks

## Troubleshooting

### Common Issues
- **Playwright errors**: Check browser installation with `playwright install`
- **API errors**: Verify API key in environment variables
- **Token limits**: Reduce `MAX_HTML_TOKENS` in config
- **Timeouts**: Increase `PAGE_WAIT_TIMEOUT`
- **Missing data**: Check Pydantic model matches HTML structure

## Code Review Checklist

- [ ] Async/await used for all I/O operations
- [ ] Type hints on all function signatures
- [ ] Docstrings for new functions/classes
- [ ] Error handling with meaningful messages
- [ ] Configuration values in config.py, not hardcoded
- [ ] Resources properly cleaned up (context managers)
- [ ] Tests added for new functionality
- [ ] No sensitive data in code
- [ ] Code follows project structure
- [ ] README updated if needed