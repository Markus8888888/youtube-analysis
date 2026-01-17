"""
Logging configuration for AI Brain
Provides structured logging across all modules
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


class LogFormatter(logging.Formatter):
    """Custom log formatter with colors for terminal output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        levelname = record.levelname
        color = self.COLORS.get(levelname, self.RESET)
        
        # Format the log message
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} | {color}{levelname:8s}{self.RESET} | {record.name:30s} | {record.getMessage()}"
        
        return log_message


def setup_logging(
    name: str,
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True
) -> logging.Logger:
    """
    Setup logger for a module
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_to_file: Write logs to file
        log_to_console: Write logs to console
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(LogFormatter())
        logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        log_file = LOG_DIR / f"{name.replace('.', '_')}.log"
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Module-level loggers
logger_brain = setup_logging("ai_brain.brain")
logger_gemini = setup_logging("ai_brain.gemini_client")
logger_chat = setup_logging("ai_brain.chat_manager")
logger_cache = setup_logging("ai_brain.cache")
logger_errors = setup_logging("ai_brain.errors")


def log_api_call(function_name: str, model: str, input_tokens: int = None):
    """Log API call with details"""
    msg = f"API Call: {function_name} using {model}"
    if input_tokens:
        msg += f" ({input_tokens} input tokens)"
    logger_gemini.info(msg)


def log_cache_hit(cache_type: str, key: str):
    """Log cache hit"""
    logger_cache.debug(f"Cache HIT ({cache_type}): {key[:16]}...")


def log_cache_miss(cache_type: str, key: str):
    """Log cache miss"""
    logger_cache.debug(f"Cache MISS ({cache_type}): {key[:16]}...")


def log_analysis_result(comment: str, result: dict, duration_ms: float):
    """Log analysis result"""
    sentiment = result.get("sentiment_score", "N/A")
    controversy = result.get("controversy_level", "N/A")
    logger_brain.info(
        f"Analysis complete: sentiment={sentiment}, controversy={controversy}, "
        f"duration={duration_ms:.1f}ms, comment_length={len(comment)}"
    )


def log_batch_analysis(batch_size: int, duration_ms: float, avg_sentiment: float):
    """Log batch analysis result"""
    logger_brain.info(
        f"Batch analysis complete: {batch_size} comments in {duration_ms:.1f}ms, "
        f"avg_sentiment={avg_sentiment:.2f}"
    )


def log_error(error_type: str, message: str, context: dict = None):
    """Log error with context"""
    msg = f"[{error_type}] {message}"
    if context:
        msg += f" | Context: {context}"
    logger_errors.error(msg)


def log_quota_exceeded(retry_wait: int):
    """Log quota exceeded event"""
    logger_errors.warning(f"API quota exceeded. Retrying in {retry_wait}s...")


def log_health_check(status: dict):
    """Log health check results"""
    logger_brain.info(f"Health check: {status}")
