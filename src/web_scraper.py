"""
Web scraping functionality using Playwright.
"""
import asyncio
from playwright.async_api import async_playwright
from typing import Optional
from config import BROWSER_ARGS, PAGE_WAIT_TIMEOUT
import logging

logger = logging.getLogger(__name__)


class WebScraperAgent:
    """Asynchronous web scraper using Playwright."""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        logger.info("WebScraperAgent instance created")

    async def init_browser(self):
        """Initialize the browser with optimized settings."""
        try:
            logger.info("Initializing Playwright browser")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=BROWSER_ARGS
            )
            self.page = await self.browser.new_page()
            logger.info("Browser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}", exc_info=True)
            raise

    async def scrape_content(self, url: str) -> str:
        """
        Scrape HTML content from a given URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            str: The HTML content of the page
            
        Raises:
            Exception: If navigation or scraping fails
        """
        if not self.page or self.page.is_closed():
            logger.warning("Page not initialized or closed, reinitializing browser")
            await self.init_browser()
        
        try:
            logger.info(f"Navigating to {url}")
            await self.page.goto(url, wait_until="load", timeout=30000)
            logger.info(f"Waiting {PAGE_WAIT_TIMEOUT}ms for dynamic content")
            await self.page.wait_for_timeout(PAGE_WAIT_TIMEOUT)
            
            content = await self.page.content()
            logger.info(f"Successfully scraped {len(content)} characters from {url}")
            return content
        except Exception as e:
            logger.error(f"Failed to scrape content from {url}: {str(e)}", exc_info=True)
            raise

    async def take_screenshot(self, path: str = "screenshot.png") -> str:
        """
        Take a full-page screenshot and save to file.
        
        Args:
            path: File path to save the screenshot
            
        Returns:
            str: The path where the screenshot was saved
        """
        try:
            logger.info(f"Taking screenshot and saving to {path}")
            await self.page.screenshot(path=path, full_page=True)
            logger.info(f"Screenshot saved to {path}")
            return path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}", exc_info=True)
            raise

    async def screenshot_buffer(self) -> bytes:
        """
        Take a screenshot and return as bytes buffer.
        
        Returns:
            bytes: The screenshot as PNG bytes
        """
        try:
            logger.info("Taking screenshot as buffer")
            screenshot_bytes = await self.page.screenshot(type="png", full_page=False)
            logger.info(f"Screenshot buffer created: {len(screenshot_bytes)} bytes")
            return screenshot_bytes
        except Exception as e:
            logger.error(f"Failed to create screenshot buffer: {str(e)}", exc_info=True)
            raise

    async def close(self):
        """Close the browser and clean up resources."""
        try:
            logger.info("Closing browser and cleaning up resources")
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            self.playwright = None
            self.browser = None
            self.page = None
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
            # Don't re-raise during cleanup

    async def __aenter__(self):
        """Async context manager entry."""
        await self.init_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()