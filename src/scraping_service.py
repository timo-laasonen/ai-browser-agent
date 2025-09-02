"""
Main scraping service that orchestrates web scraping and LLM processing.
"""
import asyncio
from typing import Tuple, Optional
from web_scraper import WebScraperAgent
from llm_processor import LLMProcessor
from models import DeeplearningCourseList


class ScrapingService:
    """Main service for orchestrating web scraping and data processing."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the scraping service."""
        self.llm_processor = LLMProcessor(api_key)
    
    async def scrape_and_process(
        self, 
        target_url: str, 
        instructions: str
    ) -> Tuple[Optional[DeeplearningCourseList], Optional[bytes]]:
        """
        Scrape a website and process the content with LLM.
        
        Args:
            target_url: The URL to scrape
            instructions: Instructions for the LLM processing
            
        Returns:
            Tuple of (processed_data, screenshot_bytes)
        """
        result = None
        screenshot = None
        
        try:
            async with WebScraperAgent() as scraper:
                # Scrape content and capture screenshot
                print("Extracting HTML Content \n")
                html_content = await scraper.scrape_content(target_url)

                print("Taking Screenshot \n")
                screenshot = await scraper.screenshot_buffer()

                # Process content with LLM
                print("Processing with LLM...")
                result = await self.llm_processor.process_html_to_structured_data(
                    html_content, instructions
                )
                print("\nGenerated Structured Response")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        return result, screenshot


# Legacy function for backward compatibility
async def webscraper(target_url: str, instructions: str):
    """
    Legacy function wrapper for backward compatibility.
    
    Args:
        target_url: The URL to scrape
        instructions: Instructions for processing
        
    Returns:
        Tuple of (result, screenshot)
    """
    service = ScrapingService()
    return await service.scrape_and_process(target_url, instructions)