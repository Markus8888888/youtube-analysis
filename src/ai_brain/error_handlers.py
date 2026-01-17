"""
Error handling and retry logic for AI Brain
Provides resilient API communication with exponential backoff
"""

import time
import logging
from functools import wraps
from typing import Callable, Any, TypeVar, Optional
import google.api_core.exceptions as api_exceptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')


class AIBrainException(Exception):
    """Base exception for AI Brain errors"""
    pass


class APIQuotaExceeded(AIBrainException):
    """Raised when API quota is exceeded"""
    pass


class APIAuthenticationError(AIBrainException):
    """Raised when API authentication fails"""
    pass


class AnalysisFailedError(AIBrainException):
    """Raised when sentiment analysis fails"""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0
) -> Callable:
    """
    Decorator for exponential backoff retry logic
    
    Args:
        max_retries: Number of retry attempts
        initial_delay: Initial wait time in seconds
        backoff_factor: Multiplier for delay between retries
        max_delay: Maximum wait time
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                
                except api_exceptions.TooManyRequests as e:
                    last_exception = APIQuotaExceeded(f"API quota exceeded: {str(e)}")
                    if attempt < max_retries:
                        logger.warning(f"Quota exceeded. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                    else:
                        raise last_exception
                
                except api_exceptions.Unauthenticated as e:
                    raise APIAuthenticationError(f"Invalid API key or authentication failed: {str(e)}")
                
                except api_exceptions.PermissionDenied as e:
                    raise APIAuthenticationError(f"Permission denied: {str(e)}")
                
                except api_exceptions.InvalidArgument as e:
                    # Don't retry on invalid arguments
                    raise AnalysisFailedError(f"Invalid argument: {str(e)}")
                
                except api_exceptions.DeadlineExceeded as e:
                    last_exception = APIQuotaExceeded(f"Request timeout: {str(e)}")
                    if attempt < max_retries:
                        logger.warning(f"Request timed out. Retrying... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                    else:
                        raise last_exception
                
                except Exception as e:
                    # Log unexpected errors but don't retry
                    logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                    raise AnalysisFailedError(f"Analysis failed: {str(e)}")
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def validate_input(text: Optional[str], min_length: int = 1, max_length: int = 10000) -> bool:
    """
    Validate input text for analysis
    
    Args:
        text: Text to validate
        min_length: Minimum text length
        max_length: Maximum text length
    
    Returns:
        True if valid, raises exception otherwise
    """
    if text is None:
        raise ValueError("Input text cannot be None")
    
    text = text.strip()
    
    if len(text) < min_length:
        raise ValueError(f"Input too short. Minimum {min_length} characters required.")
    
    if len(text) > max_length:
        raise ValueError(f"Input too long. Maximum {max_length} characters allowed.")
    
    return True


def handle_api_error(error: Exception) -> dict:
    """
    Convert API errors to user-friendly response
    
    Args:
        error: Exception from API call
    
    Returns:
        Error response dictionary
    """
    if isinstance(error, APIQuotaExceeded):
        return {
            "status": "error",
            "error_type": "quota_exceeded",
            "message": "API quota exceeded. Please try again in a moment.",
            "details": str(error)
        }
    
    elif isinstance(error, APIAuthenticationError):
        return {
            "status": "error",
            "error_type": "authentication_failed",
            "message": "Authentication failed. Check your API key.",
            "details": str(error)
        }
    
    elif isinstance(error, AnalysisFailedError):
        return {
            "status": "error",
            "error_type": "analysis_failed",
            "message": "Analysis failed. Please try with different input.",
            "details": str(error)
        }
    
    elif isinstance(error, ValueError):
        return {
            "status": "error",
            "error_type": "invalid_input",
            "message": str(error),
            "details": ""
        }
    
    else:
        return {
            "status": "error",
            "error_type": "unknown",
            "message": "An unexpected error occurred.",
            "details": str(error)
        }
