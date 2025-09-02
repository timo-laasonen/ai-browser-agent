# Web Scraping Application

A modular Python application for scraping and processing web content using Playwright and OpenAI's LLM.

## Project Structure

```
├── main.py              # Main application entry point
├── models.py            # Pydantic data models
├── web_scraper.py       # Web scraping functionality
├── llm_processor.py     # LLM processing logic
├── scraping_service.py  # Main orchestration service
├── config.py            # Configuration settings
├── helpers.py           # Helper functions (external dependency)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Components

### models.py
- **DeeplearningCourse**: Pydantic model for individual course data
- **DeeplearningCourseList**: Container for multiple courses

### web_scraper.py
- **WebScraperAgent**: Handles browser automation with Playwright
- Supports context manager for proper resource cleanup
- Configurable browser settings for optimal performance

### llm_processor.py
- **LLMProcessor**: Processes HTML content using OpenAI's structured output
- Handles token truncation and error management
- Returns strongly-typed Pydantic models

### scraping_service.py
- **ScrapingService**: Main orchestration class
- Combines web scraping and LLM processing
- Provides clean async interface

### config.py
- Centralized configuration management
- Browser settings, URLs, and LLM parameters
- Easy to modify without touching core logic

### main.py
- Application entry point
- Handles Jupyter notebook compatibility
- Example usage of the scraping service

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

3. Ensure you have the `helpers.py` file with required functions:
   - `get_openai_api_key()`
   - `visualizeCourses()`

## Usage

### Basic Usage
```python
import asyncio
from scraping_service import ScrapingService

async def scrape_courses():
    service = ScrapingService()
    result, screenshot = await service.scrape_and_process(
        "https://www.deeplearning.ai/courses",
        "Get all the courses"
    )
    return result, screenshot

# Run the scraping
result, screenshot = asyncio.run(scrape_courses())
```

### Using Individual Components
```python
from web_scraper import WebScraperAgent
from llm_processor import LLMProcessor

# Web scraping only
async with WebScraperAgent() as scraper:
    html = await scraper.scrape_content("https://example.com")
    screenshot = await scraper.screenshot_buffer()

# LLM processing only
processor = LLMProcessor()
result = await processor.process_html_to_structured_data(html, instructions)
```

## Features

- **Modular Design**: Each component has a single responsibility
- **Async/Await Support**: Efficient handling of I/O operations  
- **Context Management**: Proper resource cleanup
- **Type Safety**: Pydantic models for data validation
- **Error Handling**: Comprehensive exception handling
- **Configuration**: Centralized settings management
- **Jupyter Compatible**: Works in notebook environments

## Configuration

Modify `config.py` to adjust:
- Target URLs
- Browser settings
- LLM parameters
- Timeout values

## Error Handling

The application includes comprehensive error handling:
- Browser initialization failures
- Network timeouts
- LLM processing errors
- Resource cleanup on exceptions

## Dependencies

See `requirements.txt` for the complete list of dependencies. Key libraries:
- **playwright**: Web automation
- **openai**: LLM processing
- **pydantic**: Data validation
- **nest-asyncio**: Jupyter compatibility