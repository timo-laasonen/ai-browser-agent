"""
LLM processing functionality for structured data extraction.
"""
from openai import OpenAI
from config import DEFAULT_MODEL, MAX_HTML_TOKENS
from models import DeeplearningCourseList
from helpers import get_openai_api_key
from typing import Optional


class LLMProcessor:
    """Handles LLM-based processing of HTML content."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI client."""
        self.client = OpenAI(api_key=api_key or get_openai_api_key())
    
    async def process_html_to_structured_data(
        self, 
        html: str, 
        instructions: str,
        max_tokens: int = MAX_HTML_TOKENS
    ) -> DeeplearningCourseList:
        """
        Process HTML content using LLM to extract structured course data.
        
        Args:
            html: The HTML content to process
            instructions: Processing instructions for the LLM
            max_tokens: Maximum number of tokens to send to the LLM
            
        Returns:
            DeeplearningCourseList: Parsed course data
        """
        # Truncate HTML to stay under token limits
        truncated_html = html[:max_tokens]
        
        completion = self.client.beta.chat.completions.parse(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are an expert web scraping agent. Your task is to:
                    Extract relevant information from this HTML to JSON 
                    following these instructions:
                    {instructions}
                    
                    Extract the title, description, presenter, 
                    the image URL and course URL for each of 
                    all the courses for the deeplearning.ai website

                    Return ONLY valid JSON, no markdown or extra text.
                    """
                },
                {
                    "role": "user",
                    "content": truncated_html
                }
            ],
            temperature=0.1,
            response_format=DeeplearningCourseList,
        )
        
        return completion.choices[0].message.parsed