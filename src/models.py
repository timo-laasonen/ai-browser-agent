"""
Data models for the web scraping application.
"""
from pydantic import BaseModel
from typing import List


class DeeplearningCourse(BaseModel):
    """Model for a single deeplearning.ai course."""
    title: str
    description: str
    presenter: List[str]
    imageUrl: str
    courseURL: str


class DeeplearningCourseList(BaseModel):
    """Model for a list of deeplearning.ai courses."""
    courses: List[DeeplearningCourse]