"""
Configuration settings for the web scraping application.
"""
import os
import logging

# URLs
TARGET_URL = "https://www.deeplearning.ai/courses"
BASE_URL = "https://deeplearning.ai"

# LLM Settings
DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"
MAX_HTML_TOKENS = 150000
LLM_TEMPERATURE = 0.1

# Default instructions
DEFAULT_INSTRUCTIONS = "Get all the courses"

# Browser settings
BROWSER_ARGS = [
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-accelerated-2d-canvas",
    "--disable-gpu",
    "--no-zygote",
    "--disable-audio-output",
    "--disable-software-rasterizer",
    "--disable-webgl",
    "--disable-web-security",
    "--disable-features=LazyFrameLoading",
    "--disable-features=IsolateOrigins",
    "--disable-background-networking"
]

# Timeouts
PAGE_WAIT_TIMEOUT = 2000  # milliseconds

# Logging Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)