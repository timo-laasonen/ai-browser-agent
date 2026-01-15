"""
Main application entry point for the web scraping application.
"""
import asyncio
from scraping_service import ScrapingService
from models import DeeplearningCourseList
from helpers import visualizeCourses
from config import TARGET_URL, BASE_URL, DEFAULT_INSTRUCTIONS
import logging

logger = logging.getLogger(__name__)


async def main():
    """Main function to run the scraping application."""
    try:
        logger.info("Starting web scraping application")
        
        # Initialize the scraping service
        service = ScrapingService()
        
        # Run the scraping and processing with the response model
        result, screenshot = await service.scrape_and_process(
            TARGET_URL, 
            DEFAULT_INSTRUCTIONS,
            DeeplearningCourseList  # Pass the model class
        )
        
        # Visualize results if available
        if result and screenshot:
            logger.info("Visualizing results")
            await visualizeCourses(
                result=result,
                screenshot=screenshot,
                target_url=TARGET_URL,
                instructions=DEFAULT_INSTRUCTIONS,
                base_url=BASE_URL
            )
        else:
            logger.warning("No results to display")
            print("❌ No results to display")
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        print(f"❌ Application error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())