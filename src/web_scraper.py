"""
Web scraping functionality using Playwright.
"""
import asyncio
from playwright.async_api import async_playwright
from typing import Optional
from config import BROWSER_ARGS, PAGE_WAIT_TIMEOUT


class WebScraperAgent:
    """Asynchronous web scraper using Playwright."""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def init_browser(self):
        """Initialize the browser with optimized settings."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=BROWSER_ARGS
        )
        self.page = await self.browser.new_page()

    async def scrape_content(self, url: str) -> str:
        """Scrape HTML content from a given URL."""
        if not self.page or self.page.is_closed():
            await self.init_browser()
        
        await self.page.goto(url, wait_until="load")
        await self.page.wait_for_timeout(PAGE_WAIT_TIMEOUT)  # Wait for dynamic content
        return await self.page.content()

    async def take_screenshot(self, path: str = "screenshot.png") -> str:
        """Take a full-page screenshot and save to file."""
        await self.page.screenshot(path=path, full_page=True)
        return path

    async def screenshot_buffer(self) -> bytes:
        """Take a screenshot and return as bytes buffer."""
        screenshot_bytes = await self.page.screenshot(type="png", full_page=False)
        return screenshot_bytes

    async def close(self):
        """Close the browser and clean up resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        self.playwright = None
        self.browser = None
        self.page = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.init_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()