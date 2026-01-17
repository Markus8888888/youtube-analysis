"""
Tests for frontend components
Run with: pytest tests/test_frontend.py
"""

import pytest
from src.utils.validators import (
    validate_youtube_url,
    extract_video_id,
    validate_api_key,
    sanitize_input,
    validate_comment_count
)

class TestYouTubeURLValidation:
    """Test YouTube URL validation"""
    
    def test_valid_standard_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert validate_youtube_url(url) == True
    
    def test_valid_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert validate_youtube_url(url) == True
    
    def test_valid_mobile_url(self):
        url = "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        assert validate_youtube_url(url) == True
    
    def test_invalid_url(self):
        url = "https://google.com"
        assert validate_youtube_url(url) == False
    
    def test_empty_url(self):
        assert validate_youtube_url("") == False
        assert validate_youtube_url(None) == False
    
    def test_malformed_url(self):
        url = "not a url"
        assert validate_youtube_url(url) == False

class TestVideoIDExtraction:
    """Test video ID extraction"""
    
    def test_extract_from_standard_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_from_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_from_invalid_url(self):
        url = "https://google.com"
        assert extract_video_id(url) is None

class TestAPIKeyValidation:
    """Test API key validation"""
    
    def test_valid_youtube_key(self):
        # Mock key with correct length
        key = "A" * 39
        assert validate_api_key(key, 'youtube') == True
    
    def test_invalid_youtube_key(self):
        key = "short"
        assert validate_api_key(key, 'youtube') == False
    
    def test_empty_key(self):
        assert validate_api_key("", 'youtube') == False
        assert validate_api_key(None, 'youtube') == False

class TestInputSanitization:
    """Test input sanitization"""
    
    def test_remove_html_tags(self):
        input_text = "<script>alert('xss')</script>Hello"
        sanitized = sanitize_input(input_text)
        assert "<script>" not in sanitized
        assert "Hello" in sanitized
    
    def test_handle_empty_input(self):
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""
    
    def test_normal_text(self):
        text = "This is normal text"
        assert sanitize_input(text) == text

class TestCommentCountValidation:
    """Test comment count validation"""
    
    def test_valid_count(self):
        assert validate_comment_count(100) == 100
    
    def test_count_too_high(self):
        # Should clamp to max 200
        assert validate_comment_count(500) == 200
    
    def test_count_too_low(self):
        # Should clamp to min 10
        assert validate_comment_count(5) == 10
    
    def test_invalid_count(self):
        # Should return default 100
        assert validate_comment_count("invalid") == 100
        assert validate_comment_count(None) == 100

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])