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

from src.ai_brain.gemini_client import GeminiClient
from src.ai_brain.chat_manager import ChatManager
from src.ai_brain.prompts import (
    SENTIMENT_ANALYZER_PROMPT,
    YOUTUBE_ANALYST_BOT,
    QUERY_CATEGORIZER_PROMPT,
    INSIGHT_GENERATOR_PROMPT
)
from src.ai_brain.error_handlers import (
    retry_with_backoff,
    validate_input,
    handle_api_error,
    AIBrainException
)
from src.ai_brain.cache import get_sentiment_cache, get_batch_cache
from src.ai_brain.logger import (
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
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        self.gemini_client = GeminiClient(self.api_key)
        self.chat_manager = ChatManager(self.api_key, YOUTUBE_ANALYST_BOT)

        genai.configure(api_key=self.api_key)
        self.query_categorizer = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            system_instruction=QUERY_CATEGORIZER_PROMPT,
            generation_config={"temperature": 0.1}
        )
        self.insight_generator = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            system_instruction=INSIGHT_GENERATOR_PROMPT,
            generation_config={"temperature": 0.7}
        )

    def analyze_comments(self, comments_list):
        """
        Analyze a list of comments
        Returns: list of analysis dicts
        """
        if not comments_list:
            return []

        analyses = []
        cache = get_sentiment_cache()
        model = self.gemini_client.get_summarizer_model()

        for comment_text in comments_list:
            try:
                validate_input(comment_text)

                cached_result = cache.get(comment_text)
                if cached_result:
                    log_cache_hit("sentiment", comment_text[:32])
                    analyses.append(cached_result)
                    continue

                log_cache_miss("sentiment", comment_text[:32])

                start_time = time.time()
                response = self._call_with_timeout(
                    model.generate_content,
                    comment_text,
                    timeout=30
                )
                duration_ms = (time.time() - start_time) * 1000

                try:
                    result = json.loads(response.text)
                    cache.put(comment_text, result)
                    log_analysis_result(comment_text, result, duration_ms)
                    analyses.append(result)

                except json.JSONDecodeError:
                    error_msg = "Failed to parse AI response as JSON"
                    log_error(
                        "JSON_PARSE_ERROR",
                        error_msg,
                        {"response": response.text[:100]}
                    )
                    analyses.append({
                        "error": error_msg,
                        "raw_response": response.text[:200]
                    })

            except Exception as e:
                error_response = handle_api_error(e)
                log_error("ANALYSIS_FAILED", str(e))
                analyses.append(error_response)

        return analyses

    def analyze_batch_comments(self, comments_list):
        """
        Analyze multiple comments and aggregate sentiment
        """
        if not comments_list:
            return {"error": "Empty comments list"}

        try:
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

            analyses = self.analyze_comments(comments_list)

            for analysis in analyses:
                if "error" not in analysis:
                    results["analyses"].append(analysis)
                    sentiment_sum += analysis.get("sentiment_score", 0)
                    controversy_sum += analysis.get("controversy_level", 0)

                    for theme in analysis.get("top_3_themes", []):
                        results["aggregated"]["theme_frequency"][theme] = (
                            results["aggregated"]["theme_frequency"].get(theme, 0) + 1
                        )

            if results["analyses"]:
                results["aggregated"]["avg_sentiment"] = (
                    sentiment_sum / len(results["analyses"])
                )
                results["aggregated"]["avg_controversy"] = (
                    controversy_sum / len(results["analyses"])
                )

            batch_cache.put(comments_list, results)
            duration_ms = (time.time() - start_time) * 1000
            log_batch_analysis(
                len(comments_list),
                duration_ms,
                results["aggregated"]["avg_sentiment"]
            )

            return results

        except Exception as e:
            error_response = handle_api_error(e)
            log_error("BATCH_ANALYSIS_FAILED", str(e))
            return error_response

    def chat(self, user_message):
        try:
            validate_input(user_message, min_length=1, max_length=5000)
            response = self.chat_manager.send_message(user_message)
            return response
        except Exception as e:
            error_response = handle_api_error(e)
            log_error("CHAT_FAILED", str(e))
            return error_response.get("message", "Chat failed")

    def clear_chat_history(self):
        self.chat_manager.clear_history()

    def categorize_query(self, user_query):
        try:
            validate_input(user_query, min_length=3)
            response = self._call_with_timeout(
                self.query_categorizer.generate_content,
                user_query,
                timeout=10
            )
            category = response.text.strip().lower()
            return category if category else "general"
        except Exception:
            return "general"

    def generate_insights(self, analytics_data):
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
        batch_analysis = self.analyze_batch_comments(comments_list)

        report = {
            "status": "success",
            "comment_count": batch_analysis["total_comments"],
            "sentiment_analysis": batch_analysis["aggregated"],
            "individual_analyses": batch_analysis["analyses"]
        }

        if include_insights:
            report["insights"] = self.generate_insights(
                batch_analysis["aggregated"]
            )

        return report

    def health_check(self):
        try:
            analysis = self.analyze_comments(["Great video!"])[0]
            chat_response = self.chat("Hello!")
            category = self.categorize_query("How are you?")

            health = {
                "status": "healthy",
                "sentiment_analysis": "ok" if "error" not in analysis else "failed",
                "chatbot": "ok" if isinstance(chat_response, str) else "failed",
                "query_categorization": "ok" if category else "failed",
                "api_key": "configured" if self.api_key else "missing",
                "cache_status": "enabled"
            }

            log_health_check(health)
            return health

        except Exception as e:
            log_error("HEALTH_CHECK_FAILED", str(e))
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    def _call_with_timeout(func, *args, timeout=30, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise

    def get_cache_stats(self):
        sentiment_cache = get_sentiment_cache()
        return {"sentiment_cache": sentiment_cache.get_stats()}

    def clear_caches(self):
        get_sentiment_cache().clear()
        get_batch_cache().clear()
        logger.info("All caches cleared")
