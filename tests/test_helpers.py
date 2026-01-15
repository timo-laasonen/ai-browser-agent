"""
Unit tests for the helpers module.

Tests cover environment configuration, API client creation,
and data visualization functions.
"""

import os
import unittest
from unittest.mock import patch, MagicMock, Mock
import base64
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from helpers import (
    load_env,
    get_openai_api_key,
    get_openai_client,
    get_multi_on_api_key,
    get_multi_on_client,
    _build_table_html,
    _create_screenshot_html,
)


class TestEnvironmentConfiguration(unittest.TestCase):
    """Test cases for environment configuration functions."""
    
    @patch('helpers.load_dotenv')
    @patch('helpers.find_dotenv')
    def test_load_env_calls_dotenv_functions(self, mock_find, mock_load):
        """Test that load_env properly calls dotenv functions."""
        mock_find.return_value = '.env'
        load_env()
        
        mock_find.assert_called_once()
        mock_load.assert_called_once_with('.env')
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key-123'}, clear=True)
    @patch('helpers.load_env')
    def test_get_openai_api_key_returns_key(self, mock_load_env):
        """Test retrieving OpenAI API key from environment."""
        result = get_openai_api_key()
        
        self.assertEqual(result, 'test-key-123')
        mock_load_env.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('helpers.load_env')
    def test_get_openai_api_key_returns_none_when_missing(self, mock_load_env):
        """Test that None is returned when API key is not set."""
        result = get_openai_api_key()
        
        self.assertIsNone(result)
    
    @patch.dict(os.environ, {'MULTION_API_KEY': 'multion-key-456'}, clear=True)
    @patch('helpers.load_env')
    def test_get_multi_on_api_key_returns_key(self, mock_load_env):
        """Test retrieving MultiOn API key from environment."""
        result = get_multi_on_api_key()
        
        self.assertEqual(result, 'multion-key-456')
        mock_load_env.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('helpers.load_env')
    def test_get_multi_on_api_key_returns_none_when_missing(self, mock_load_env):
        """Test that None is returned when MultiOn API key is not set."""
        result = get_multi_on_api_key()
        
        self.assertIsNone(result)


class TestClientCreation(unittest.TestCase):
    """Test cases for API client creation functions."""
    
    @patch('helpers.OpenAI')
    @patch('helpers.get_openai_api_key')
    def test_get_openai_client_creates_client(self, mock_get_key, mock_openai_class):
        """Test successful OpenAI client creation."""
        mock_get_key.return_value = 'valid-key'
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        result = get_openai_client()
        
        mock_get_key.assert_called_once()
        mock_openai_class.assert_called_once_with(api_key='valid-key')
        self.assertEqual(result, mock_client)
    
    @patch('helpers.get_openai_api_key')
    def test_get_openai_client_raises_error_when_no_key(self, mock_get_key):
        """Test that ValueError is raised when API key is missing."""
        mock_get_key.return_value = None
        
        with self.assertRaises(ValueError) as context:
            get_openai_client()
        
        self.assertIn('OPENAI_API_KEY not found', str(context.exception))
    
    @patch('helpers.MultiOn')
    @patch('helpers.get_multi_on_api_key')
    def test_get_multi_on_client_creates_client(self, mock_get_key, mock_multion_class):
        """Test successful MultiOn client creation."""
        mock_get_key.return_value = 'valid-multion-key'
        mock_client = MagicMock()
        mock_multion_class.return_value = mock_client
        
        result = get_multi_on_client()
        
        mock_get_key.assert_called_once()
        mock_multion_class.assert_called_once_with(api_key='valid-multion-key')
        self.assertEqual(result, mock_client)
    
    @patch('helpers.get_multi_on_api_key')
    def test_get_multi_on_client_raises_error_when_no_key(self, mock_get_key):
        """Test that ValueError is raised when MultiOn API key is missing."""
        mock_get_key.return_value = None
        
        with self.assertRaises(ValueError) as context:
            get_multi_on_client()
        
        self.assertIn('MULTION_API_KEY not found', str(context.exception))


class TestTableBuilder(unittest.TestCase):
    """Test cases for HTML table building function."""
    
    def test_build_table_html_with_empty_list(self):
        """Test table building with empty course list."""
        result = _build_table_html([], 'https://example.com')
        
        self.assertEqual(result, "<p>No course data available.</p>")
    
    def test_build_table_html_with_course_data(self):
        """Test table building with valid course data."""
        courses_data = [
            {
                'title': 'Python Basics',
                'courseURL': '/courses/python-101',
                'description': 'Learn Python from scratch'
            }
        ]
        base_url = 'https://example.com'
        
        result = _build_table_html(courses_data, base_url)
        
        # Verify table structure
        self.assertIn('<table', result)
        self.assertIn('<thead>', result)
        self.assertIn('<tbody>', result)
        self.assertIn('</table>', result)
        
        # Verify headers
        self.assertIn('title', result)
        self.assertIn('courseURL', result)
        self.assertIn('description', result)
        
        # Verify clickable link was created
        self.assertIn('<a href="https://example.com/courses/python-101"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('Python Basics</a>', result)
    
    def test_build_table_html_with_image_url(self):
        """Test table building with imageUrl field."""
        courses_data = [
            {
                'title': 'Course with Image',
                'imageUrl': 'https://example.com/image.png'
            }
        ]
        
        result = _build_table_html(courses_data, 'https://example.com')
        
        # Verify image tag is created
        self.assertIn('<img src="https://example.com/image.png"', result)
        self.assertIn('alt="Course Image"', result)
        self.assertIn('max-width:100px', result)
    
    def test_build_table_html_with_list_values(self):
        """Test table building with list-type values."""
        courses_data = [
            {
                'title': 'Multi-Tag Course',
                'tags': ['Python', 'Data Science', 'AI']
            }
        ]
        
        result = _build_table_html(courses_data, 'https://example.com')
        
        # Verify list is joined with commas
        self.assertIn('Python, Data Science, AI', result)
    
    def test_build_table_html_without_course_url(self):
        """Test table building when courseURL is missing."""
        courses_data = [
            {
                'title': 'Course Without URL',
                'courseURL': None,
                'description': 'A course without a URL'
            }
        ]
        
        result = _build_table_html(courses_data, 'https://example.com')
        
        # Should not modify None courseURL
        self.assertIn('Course Without URL', result)
        # Should not create a link for None URL
        self.assertNotIn('<a href="https://example.com/None"', result)


class TestScreenshotHTML(unittest.TestCase):
    """Test cases for screenshot HTML creation function."""
    
    def test_create_screenshot_html_encodes_correctly(self):
        """Test that screenshot bytes are properly encoded to base64."""
        test_bytes = b'fake-image-data-123'
        expected_b64 = base64.b64encode(test_bytes).decode('utf-8')
        
        result = _create_screenshot_html(test_bytes)
        
        # Verify structure
        self.assertIn('<img src="data:image/png;base64,', result)
        self.assertIn(f'{expected_b64}', result)
        self.assertIn('alt="Website Screenshot"', result)
        self.assertIn('max-width:100%', result)
    
    def test_create_screenshot_html_with_empty_bytes(self):
        """Test screenshot HTML creation with empty bytes."""
        test_bytes = b''
        expected_b64 = base64.b64encode(test_bytes).decode('utf-8')
        
        result = _create_screenshot_html(test_bytes)
        
        self.assertIn('<img src="data:image/png;base64,', result)
        # Empty bytes should produce empty base64 string
        self.assertIn(f'{expected_b64}', result)


class TestVisualizeCourses(unittest.TestCase):
    """Test cases for visualize_courses function."""
    
    @patch('helpers.display')
    @patch('helpers.HTML')
    @patch('helpers.Markdown')
    def test_visualize_courses_with_no_result(self, mock_markdown, mock_html, mock_display):
        """Test visualize_courses when result is None."""
        import asyncio
        from helpers import visualize_courses
        
        async def run_test():
            await visualize_courses(None, b'screenshot', 'url', 'instructions', 'base')
        
        asyncio.run(run_test())
        
        # Should display "No results available" message
        mock_markdown.assert_called_once_with("### No results available")
        mock_display.assert_called_once()
    
    @patch('helpers.display')
    @patch('helpers.HTML')
    @patch('helpers.Markdown')
    @patch('helpers._create_screenshot_html')
    @patch('helpers._build_table_html')
    def test_visualize_courses_with_valid_result(
        self, mock_build_table, mock_create_screenshot, 
        mock_markdown, mock_html, mock_display
    ):
        """Test visualize_courses with valid course data."""
        import asyncio
        from helpers import visualize_courses
        
        # Mock course objects
        mock_course = Mock()
        mock_course.model_dump.return_value = {
            'title': 'Test Course',
            'courseURL': '/course/1'
        }
        
        mock_result = Mock()
        mock_result.courses = [mock_course]
        
        mock_build_table.return_value = '<table>Test Table</table>'
        mock_create_screenshot.return_value = '<img src="data:image/png;base64,test"/>'
        
        async def run_test():
            await visualize_courses(
                mock_result,
                b'screenshot',
                'https://example.com',
                'scrape courses',
                'https://example.com'
            )
        
        asyncio.run(run_test())
        
        # Verify course data was dumped
        mock_course.model_dump.assert_called_once()
        
        # Verify table and screenshot were created
        mock_build_table.assert_called_once()
        mock_create_screenshot.assert_called_once_with(b'screenshot')
        
        # Verify display was called for both sections
        self.assertEqual(mock_display.call_count, 4)  # 2 markdown headers + 2 HTML displays


def run_tests():
    """Run all unit tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == '__main__':
    unittest.main()
