"""
Helper utilities for the AI Browser Agent.

This module provides utility functions for API client initialization,
environment variable management, and data visualization.
"""

import os
from typing import Optional, List, Dict, Any
import base64
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from multion.client import MultiOn
from io import BytesIO
from PIL import Image
from IPython.display import display, HTML, Markdown


# Environment Configuration
def load_env() -> None:
    """Load environment variables from .env file."""
    load_dotenv(find_dotenv())


def get_openai_api_key() -> Optional[str]:
    """
    Retrieve OpenAI API key from environment variables.
    
    Returns:
        Optional[str]: The OpenAI API key, or None if not found.
    """
    load_env()
    return os.getenv("OPENAI_API_KEY")


def get_openai_client() -> OpenAI:
    """
    Create and return an OpenAI client instance.
    
    Returns:
        OpenAI: Configured OpenAI client.
    
    Raises:
        ValueError: If API key is not found in environment.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)


def get_multi_on_api_key() -> Optional[str]:
    """
    Retrieve MultiOn API key from environment variables.
    
    Returns:
        Optional[str]: The MultiOn API key, or None if not found.
    """
    load_env()
    return os.getenv("MULTION_API_KEY")


def get_multi_on_client() -> MultiOn:
    """
    Create and return a MultiOn client instance.
    
    Returns:
        MultiOn: Configured MultiOn client.
    
    Raises:
        ValueError: If API key is not found in environment.
    """
    api_key = get_multi_on_api_key()
    if not api_key:
        raise ValueError("MULTION_API_KEY not found in environment variables")
    return MultiOn(api_key=api_key)


# Visualization Functions
def _build_table_html(courses_data: List[Dict[str, Any]], base_url: str) -> str:
    """
    Build an HTML table from course data.
    
    Args:
        courses_data: List of course dictionaries.
        base_url: Base URL for course links.
    
    Returns:
        str: HTML table string.
    """
    if not courses_data:
        return "<p>No course data available.</p>"
    
    # Modify course URLs to create clickable links
    for course in courses_data:
        if course.get('courseURL'):
            course['courseURL'] = (
                f'<a href="{base_url}{course["courseURL"]}" target="_blank">'
                f'{course["title"]}</a>'
            )
    
    # Build table structure
    headers = courses_data[0].keys()
    table_html_parts = [
        '<table style="border-collapse: collapse; width: 100%;">',
        '<thead><tr>'
    ]
    
    # Add headers
    for header in headers:
        table_html_parts.append(
            f'<th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'
            f'{header}</th>'
        )
    
    table_html_parts.append('</tr></thead><tbody>')
    
    # Add rows
    for course in courses_data:
        table_html_parts.append('<tr>')
        for header in headers:
            value = course[header]
            
            # Handle different value types
            if header == "imageUrl":
                value = (
                    f'<img src="{value}" alt="Course Image" '
                    f'style="max-width:100px; height:auto;">'
                )
            elif isinstance(value, list):
                value = ', '.join(str(item) for item in value)
            
            table_html_parts.append(
                f'<td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'
                f'{value}</td>'
            )
        table_html_parts.append('</tr>')
    
    table_html_parts.append('</tbody></table>')
    return ''.join(table_html_parts)


def _create_screenshot_html(screenshot: bytes) -> str:
    """
    Convert screenshot bytes to base64-encoded HTML image tag.
    
    Args:
        screenshot: Screenshot image as bytes.
    
    Returns:
        str: HTML img tag with base64-encoded image.
    """
    img_b64 = base64.b64encode(screenshot).decode('utf-8')
    return (
        f'<img src="data:image/png;base64,{img_b64}" '
        f'alt="Website Screenshot" style="max-width:100%; height:auto;">'
    )


async def visualize_courses(
    result: Any,
    screenshot: bytes,
    target_url: str,
    instructions: str,
    base_url: str
) -> None:
    """
    Display scraped course data and website screenshot in Jupyter notebook.
    
    Args:
        result: Course data result object with a 'courses' attribute.
        screenshot: Screenshot image as bytes.
        target_url: Target URL that was scraped.
        instructions: Scraping instructions used.
        base_url: Base URL for constructing full course URLs.
    """
    if not result:
        display(Markdown("### No results available"))
        return
    
    # Convert courses to dictionaries
    courses_data = [course.model_dump() for course in result.courses]
    
    # Display course data table
    display(Markdown("### Scraped Course Data:"))
    table_html = _build_table_html(courses_data, base_url)
    display(HTML(table_html))
    
    # Display screenshot
    display(Markdown("### Website Screenshot:"))
    screenshot_html = _create_screenshot_html(screenshot)
    display(HTML(screenshot_html))


