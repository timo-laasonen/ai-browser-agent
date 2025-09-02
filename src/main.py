"""
Main application entry point for the web scraping application.
"""
import asyncio
from scraping_service import ScrapingService
from helpers import visualizeCourses
from config import TARGET_URL, BASE_URL, DEFAULT_INSTRUCTIONS


async def main():
    """Main function to run the scraping application."""
    try:
        # Initialize the scraping service
        service = ScrapingService()
        
        # Run the scraping and processing
        result, screenshot = await service.scrape_and_process(
            TARGET_URL, 
            DEFAULT_INSTRUCTIONS
        )
        
        # Visualize results if available
        if result and screenshot:
            await visualizeCourses(
                result=result,
                screenshot=screenshot,
                target_url=TARGET_URL,
                instructions=DEFAULT_INSTRUCTIONS,
                base_url=BASE_URL
            )
        else:
            print("❌ No results to display")
            
    except Exception as e:
        print(f"❌ Application error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())