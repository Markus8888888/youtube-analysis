"""
AI Brain Integration Module
Orchestrates all AI components: sentiment analysis, chat, and insights
With error handling, caching, logging, and production optimizations
"""

import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai
from gemini_client import GeminiClient
from chat_manager import ChatManager
from prompts import (
    SENTIMENT_ANALYZER_PROMPT,
    YOUTUBE_ANALYST_BOT,
    QUERY_CATEGORIZER_PROMPT,
    INSIGHT_GENERATOR_PROMPT
)
from error_handlers import (
    retry_with_backoff,
    validate_input,
    handle_api_error,
    AIBrainException
)
from cache import get_sentiment_cache, get_batch_cache
from logger import (
    setup_logging,
    log_api_call,
    log_cache_hit,
    log_cache_miss,
    log_analysis_result,
    log_batch_analysis,
    log_error,
    log_health_check
)

load_dotenv()
logger = setup_logging("ai_brain.brain")


class AIBrain:
    """
    The central orchestrator for all AI operations.
    
    Tasks:
    1. Sentiment Analysis - Extract sentiment, themes, controversy from comments
    2. Chatbot - Have conversations about video analytics
    3. Query Routing - Categorize user questions
    4. Insight Generation - Create actionable recommendations
    """

    def __init__(self):
        """Initialize all AI components"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Initialize components
        self.gemini_client = GeminiClient(self.api_key)
        self.chat_manager = ChatManager(self.api_key, YOUTUBE_ANALYST_BOT)
        
        # Setup additional models for specialized tasks
        genai.configure(api_key=self.api_key)
        self.query_categorizer = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=QUERY_CATEGORIZER_PROMPT,
            generation_config={"temperature": 0.1}  # Low for categorization precision
        )
        self.insight_generator = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=INSIGHT_GENERATOR_PROMPT,
            generation_config={"temperature": 0.7}  # Higher for creative insights
        )

    def analyze_comments(self, comment_text):
        """
        Task 1: Analyze a single comment or batch of comments
        Returns: JSON with sentiment_score, themes, controversy_level
        """
        try:
            # Validate input
            validate_input(comment_text)
            
            # Check cache first
            cache = get_sentiment_cache()
            cached_result = cache.get(comment_text)
            if cached_result:
                log_cache_hit("sentiment", comment_text[:32])
                return cached_result
            
            log_cache_miss("sentiment", comment_text[:32])
            
            # Call API
            start_time = time.time()
            model = self.gemini_client.get_summarizer_model()
            response = self._call_with_timeout(
                model.generate_content,
                comment_text,
                timeout=30
            )
            duration_ms = (time.time() - start_time) * 1000
            
            # Parse JSON response
            try:
                result = json.loads(response.text)
                
                # Cache the result
                cache.put(comment_text, result)
                
                # Log success
                log_analysis_result(comment_text, result, duration_ms)
                
                return result
            
            except json.JSONDecodeError:
                error_msg = "Failed to parse AI response as JSON"
                log_error("JSON_PARSE_ERROR", error_msg, {"response": response.text[:100]})
                return {
                    "error": error_msg,
                    "raw_response": response.text[:200]
                }
        
        except Exception as e:
            error_response = handle_api_error(e)
            log_error("ANALYSIS_FAILED", str(e))
            return error_response

    def analyze_batch_comments(self, comments_list):
        """
        Analyze multiple comments and aggregate sentiment
        Returns: Overall sentiment stats and top themes
        """
        if not comments_list:
            return {"error": "Empty comments list"}
        
        try:
            # Check batch cache
            batch_cache = get_batch_cache()
            cached_result = batch_cache.get(comments_list)
            if cached_result:
                logger.info(f"Batch cache hit for {len(comments_list)} comments")
                return cached_result
            
            start_time = time.time()
            
            results = {
                "total_comments": len(comments_list),
                "analyses": [],
                "aggregated": {
                    "avg_sentiment": 0,
                    "avg_controversy": 0,
                    "theme_frequency": {}
                }
            }
            
            sentiment_sum = 0
            controversy_sum = 0
            
            for comment in comments_list:
                analysis = self.analyze_comments(comment)
                if "error" not in analysis:
                    results["analyses"].append(analysis)
                    sentiment_sum += analysis.get("sentiment_score", 0)
                    controversy_sum += analysis.get("controversy_level", 0)
                    
                    # Track theme frequencies
                    for theme in analysis.get("top_3_themes", []):
                        results["aggregated"]["theme_frequency"][theme] = \
                            results["aggregated"]["theme_frequency"].get(theme, 0) + 1
            
            # Calculate averages
            if results["analyses"]:
                results["aggregated"]["avg_sentiment"] = sentiment_sum / len(results["analyses"])
                results["aggregated"]["avg_controversy"] = controversy_sum / len(results["analyses"])
            
            # Cache and log
            batch_cache.put(comments_list, results)
            duration_ms = (time.time() - start_time) * 1000
            log_batch_analysis(len(comments_list), duration_ms, results["aggregated"]["avg_sentiment"])
            
            return results
        
        except Exception as e:
            error_response = handle_api_error(e)
            log_error("BATCH_ANALYSIS_FAILED", str(e))
            return error_response

    def chat(self, user_message):
        """
        Task 2: Conversational interface for analytics discussion
        Maintains conversation history automatically
        """
        try:
            validate_input(user_message, min_length=1, max_length=5000)
            logger.info(f"Chat message received: {len(user_message)} characters")
            response = self.chat_manager.send_message(user_message)
            logger.info(f"Chat response: {len(response)} characters")
            return response
        except Exception as e:
            error_response = handle_api_error(e)
            log_error("CHAT_FAILED", str(e))
            return error_response.get("message", "Chat failed")

    def clear_chat_history(self):
        """Reset conversation history"""
        self.chat_manager.clear_history()

    def categorize_query(self, user_query):
        """
        Task 3: Route user query to appropriate analysis type
        Returns: Category (sentiment_analysis, engagement_analysis, etc.)
        """
        try:
            validate_input(user_query, min_length=3)
            logger.info(f"Categorizing query: {user_query[:50]}...")
            
            response = self._call_with_timeout(
                self.query_categorizer.generate_content,
                user_query,
                timeout=10
            )
            category = response.text.strip().lower()
            
            valid_categories = [
                "sentiment_analysis",
                "engagement_analysis", 
                "content_analysis",
                "general"
            ]
            
            if category in valid_categories:
                logger.info(f"Query categorized as: {category}")
                return category
            else:
                logger.warning(f"Unknown category '{category}', defaulting to 'general'")
                return "general"
        
        except Exception as e:
            log_error("CATEGORIZATION_FAILED", str(e))
            logger.warning("Defaulting to 'general' category due to error")
            return "general"

    def generate_insights(self, analytics_data):
        """
        Task 4: Create actionable recommendations from analytics
        Input: Analytics data (sentiment, engagement, themes, etc.)
        Returns: List of insights and recommendations
        """
        try:
            prompt = f"""
Here is the video analytics data:
{json.dumps(analytics_data, indent=2)}

Based on this data, provide 3-5 actionable insights for the creator.
            """
            response = self.insight_generator.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"

    def full_analysis(self, comments_list, include_insights=True):
        """
        Complete end-to-end analysis pipeline
        1. Analyze all comments
        2. Aggregate sentiment and themes
        3. Generate insights
        
        Returns: Complete analysis report
        """
        # Step 1: Batch analysis
        batch_analysis = self.analyze_batch_comments(comments_list)
        
        report = {
            "status": "success",
            "comment_count": batch_analysis["total_comments"],
            "sentiment_analysis": batch_analysis["aggregated"],
            "individual_analyses": batch_analysis["analyses"]
        }
        
        # Step 2: Generate insights if requested
        if include_insights:
            insights = self.generate_insights(batch_analysis["aggregated"])
            report["insights"] = insights
        
        return report

    def health_check(self):
        """Verify all AI components are working"""
        try:
            logger.info("Starting health check...")
            
            # Test sentiment analysis
            test_comment = "Great video!"
            analysis = self.analyze_comments(test_comment)
            
            # Test chat
            chat_response = self.chat("Hello!")
            
            # Test categorization
            category = self.categorize_query("How are you?")
            
            health = {
                "status": "healthy",
                "sentiment_analysis": "ok" if "error" not in analysis else "failed",
                "chatbot": "ok" if isinstance(chat_response, str) and len(chat_response) > 0 else "failed",
                "query_categorization": "ok" if category in ["sentiment_analysis", "engagement_analysis", "content_analysis", "general"] else "failed",
                "api_key": "configured" if self.api_key else "missing",
                "cache_status": "enabled"
            }
            
            log_health_check(health)
            logger.info("Health check complete")
            
            return health
        
        except Exception as e:
            health = {
                "status": "unhealthy",
                "error": str(e),
                "api_key": "configured" if self.api_key else "missing"
            }
            log_error("HEALTH_CHECK_FAILED", str(e))
            return health
    
    @staticmethod
    def _call_with_timeout(func, *args, timeout=30, **kwargs):
        """
        Call a function with timeout (for production safety)
        Note: True timeout requires threading/multiprocessing
        This is a placeholder for integration with timeout libraries
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise
    
    def get_cache_stats(self):
        """Get caching statistics"""
        sentiment_cache = get_sentiment_cache()
        return {
            "sentiment_cache": sentiment_cache.get_stats()
        }
    
    def clear_caches(self):
        """Clear all caches"""
        get_sentiment_cache().clear()
        get_batch_cache().clear()
        logger.info("All caches cleared")
