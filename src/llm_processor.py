"""
LLM processing functionality for structured data extraction.
"""
from openai import AsyncOpenAI
from config import DEFAULT_MODEL, MAX_HTML_TOKENS
from helpers import get_openai_api_key
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
import tiktoken
import logging

# Create a type variable for generic Pydantic models
T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)


class LLMProcessor:
    """Handles LLM-based processing of HTML content."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI async client."""
        self.client = AsyncOpenAI(api_key=api_key or get_openai_api_key())
        logger.info("LLMProcessor initialized with AsyncOpenAI client")
    
    def _count_tokens(self, text: str, model: str = DEFAULT_MODEL) -> int:
        """
        Count the number of tokens in a text string.
        
        Args:
            text: The text to count tokens for
            model: The model to use for encoding
            
        Returns:
            int: Number of tokens
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"Failed to count tokens with tiktoken: {e}. Falling back to character estimate.")
            # Fallback: rough estimate of 4 characters per token
            return len(text) // 4
    
    def _truncate_html(self, html: str, max_tokens: int, model: str = DEFAULT_MODEL) -> str:
        """
        Intelligently truncate HTML to stay within token limits.
        
        Args:
            html: The HTML content to truncate
            max_tokens: Maximum number of tokens allowed
            model: The model to use for token counting
            
        Returns:
            str: Truncated HTML
        """
        token_count = self._count_tokens(html, model)
        
        if token_count <= max_tokens:
            logger.info(f"HTML is {token_count} tokens, within limit of {max_tokens}")
            return html
        
        logger.warning(f"HTML has {token_count} tokens, truncating to {max_tokens}")
        
        # Binary search to find the right length
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(html)
        truncated_tokens = tokens[:max_tokens]
        truncated_html = encoding.decode(truncated_tokens)
        
        logger.info(f"Truncated HTML to {len(truncated_tokens)} tokens")
        return truncated_html
    
    async def process_html_to_structured_data(
        self, 
        html: str, 
        instructions: str,
        response_model: Type[T],
        max_tokens: int = MAX_HTML_TOKENS,
        model: str = DEFAULT_MODEL
    ) -> T:
        """
        Process HTML content using LLM to extract structured data.
        
        Args:
            html: The HTML content to process
            instructions: Processing instructions for the LLM
            response_model: Pydantic model class defining the expected response structure
            max_tokens: Maximum number of tokens to send to the LLM
            model: OpenAI model to use for processing
            
        Returns:
            Instance of response_model with parsed data
            
        Raises:
            ValueError: If API key is missing or invalid
            Exception: If LLM processing fails
        """
        try:
            logger.info(f"Processing HTML with instructions: {instructions[:100]}...")
            
            # Truncate HTML properly using token counting
            truncated_html = self._truncate_html(html, max_tokens, model)
            
            # Build a generic system prompt
            system_content = f"""You are an expert web scraping agent. 
Extract relevant information from the provided HTML content following these instructions:

{instructions}

Return the data in the specified JSON format. Be thorough and accurate."""
            
            logger.info(f"Sending request to OpenAI API with model {model}")
            
            completion = await self.client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_content
                    },
                    {
                        "role": "user",
                        "content": truncated_html
                    }
                ],
                temperature=0.1,
                response_format=response_model,
            )
            
            logger.info("Successfully received structured response from OpenAI")
            return completion.choices[0].message.parsed
            
        except Exception as e:
            logger.error(f"LLM processing failed: {str(e)}", exc_info=True)
            raise