"""
Caching system for AI Brain
Reduces redundant API calls and improves performance
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CacheEntry:
    """Represents a single cached analysis result"""
    
    def __init__(self, result: dict, ttl_hours: int = 24):
        """
        Args:
            result: The cached analysis result
            ttl_hours: Time to live in hours
        """
        self.result = result
        self.created_at = datetime.now()
        self.ttl = timedelta(hours=ttl_hours)
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return datetime.now() > self.created_at + self.ttl
    
    def get_age_hours(self) -> float:
        """Get cache entry age in hours"""
        return (datetime.now() - self.created_at).total_seconds() / 3600


class SentimentCache:
    """
    LRU cache for sentiment analysis results
    
    Reduces API calls for repeated comments or similar text
    Automatically expires entries after TTL
    """
    
    def __init__(self, max_size: int = 1000, ttl_hours: int = 24):
        """
        Args:
            max_size: Maximum number of cached items
            ttl_hours: Cache entry time-to-live in hours
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl_hours = ttl_hours
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    @staticmethod
    def _hash_text(text: str) -> str:
        """Generate cache key from text"""
        normalized = text.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, text: str) -> Optional[dict]:
        """
        Retrieve cached analysis result
        
        Args:
            text: Input text to look up
        
        Returns:
            Cached result or None if not found/expired
        """
        key = self._hash_text(text)
        
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        if entry.is_expired():
            del self.cache[key]
            self.misses += 1
            logger.debug(f"Cache expired for key: {key}")
            return None
        
        self.hits += 1
        logger.debug(f"Cache hit for key: {key}")
        return entry.result
    
    def put(self, text: str, result: dict) -> None:
        """
        Store analysis result in cache
        
        Args:
            text: Original input text
            result: Analysis result to cache
        """
        # Don't cache error results
        if "error" in result:
            logger.debug("Skipping cache for error result")
            return
        
        key = self._hash_text(text)
        
        # Evict oldest entry if at max capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_oldest()
        
        self.cache[key] = CacheEntry(result, self.ttl_hours)
        logger.debug(f"Cached result for key: {key}")
    
    def _evict_oldest(self) -> None:
        """Remove oldest entry from cache (LRU)"""
        if not self.cache:
            return
        
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k].created_at
        )
        del self.cache[oldest_key]
        self.evictions += 1
        logger.debug(f"Evicted oldest cache entry: {oldest_key}")
    
    def clear(self) -> None:
        """Clear all cached entries"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "evictions": self.evictions,
            "ttl_hours": self.ttl_hours
        }
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns count removed."""
        expired_keys = [
            k for k, v in self.cache.items() if v.is_expired()
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)


class BatchCache:
    """
    Cache for batch analysis results
    Useful for storing aggregated sentiment over time
    """
    
    def __init__(self, max_size: int = 100, ttl_hours: int = 48):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl_hours = ttl_hours
    
    @staticmethod
    def _hash_batch(comments: list) -> str:
        """Generate cache key from comments list"""
        # Create deterministic hash from sorted comments
        normalized = json.dumps(
            sorted([c.strip().lower() for c in comments]),
            sort_keys=True
        )
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, comments: list) -> Optional[dict]:
        """Retrieve cached batch analysis"""
        key = self._hash_batch(comments)
        
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if entry.is_expired():
            del self.cache[key]
            return None
        
        logger.debug(f"Batch cache hit for {len(comments)} comments")
        return entry.result
    
    def put(self, comments: list, result: dict) -> None:
        """Store batch analysis result"""
        if "error" in result:
            return
        
        key = self._hash_batch(comments)
        
        if len(self.cache) >= self.max_size:
            # Remove oldest
            oldest_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k].created_at
            )
            del self.cache[oldest_key]
        
        self.cache[key] = CacheEntry(result, self.ttl_hours)
        logger.debug(f"Cached batch result for {len(comments)} comments")
    
    def clear(self) -> None:
        """Clear all cached entries"""
        self.cache.clear()


# Global cache instances
_sentiment_cache = SentimentCache(max_size=1000, ttl_hours=24)
_batch_cache = BatchCache(max_size=100, ttl_hours=48)


def get_sentiment_cache() -> SentimentCache:
    """Get global sentiment cache instance"""
    return _sentiment_cache


def get_batch_cache() -> BatchCache:
    """Get global batch cache instance"""
    return _batch_cache
