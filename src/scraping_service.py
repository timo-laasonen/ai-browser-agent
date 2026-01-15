"""
Main scraping service that orchestrates web scraping and LLM processing.
"""
import asyncio
from typing import Tuple, Optional, Type, TypeVar
from web_scraper import WebScraperAgent
from llm_processor import LLMProcessor
from pydantic import BaseModel
import logging

# Create a type variable for generic Pydantic models
T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)


class ScrapingService:
    """Main service for orchestrating web scraping and data processing."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the scraping service."""
        self.llm_processor = LLMProcessor(api_key)
        logger.info("ScrapingService initialized")
    
    async def scrape_and_process(
        self, 
        target_url: str, 
        instructions: str,
        response_model: Type[T]
    ) -> Tuple[Optional[T], Optional[bytes]]:
        """
        Scrape a website and process the content with LLM.
        
        Args:
            target_url: The URL to scrape
            instructions: Instructions for the LLM processing
            response_model: Pydantic model class defining expected response structure
            
        Returns:
            Tuple of (processed_data, screenshot_bytes)
            
        Raises:
            Exception: Re-raises any exceptions that occur during scraping or processing
        """
        result = None
        screenshot = None
        
        logger.info(f"Starting scrape and process for URL: {target_url}")
        
        try:
            async with WebScraperAgent() as scraper:
                # Scrape content and capture screenshot
                logger.info("Extracting HTML content")
                print("Extracting HTML Content \n")
                html_content = await scraper.scrape_content(target_url)
                logger.info(f"Successfully extracted {len(html_content)} characters of HTML")

                logger.info("Taking screenshot")
                print("Taking Screenshot \n")
                screenshot = await scraper.screenshot_buffer()
                logger.info(f"Screenshot captured: {len(screenshot)} bytes")

                # Process content with LLM
                logger.info("Processing HTML with LLM")
                print("Processing with LLM...")
                result = await self.llm_processor.process_html_to_structured_data(
                    html_content, instructions, response_model
                )
                logger.info("Successfully generated structured response")
                print("\nGenerated Structured Response")
                
        except Exception as e:
            logger.error(f"Scraping and processing failed: {str(e)}", exc_info=True)
            print(f"❌ Error: {str(e)}")
            # Re-raise the exception so calling code can handle it appropriately
            raise
        
        return result, screenshot


# Legacy function for backward compatibility
async def webscraper(target_url: str, instructions: str, response_model: Type[T]) -> Tuple[Optional[T], Optional[bytes]]:
    """
    Legacy function wrapper for backward compatibility.
    
    Args:
        target_url: The URL to scrape
        instructions: Instructions for processing
        response_model: Pydantic model class defining expected response structure
        
    Returns:
        Tuple of (result, screenshot)
    """
    logger.warning("Using legacy webscraper function. Consider using ScrapingService directly.")
    service = ScrapingService()
    return await service.scrape_and_process(target_url, instructions, response_model)