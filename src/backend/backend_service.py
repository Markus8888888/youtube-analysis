"""
Backend Service - Connects YouTube API and AI Brain
"""
from typing import Any, Dict, List
from src.data_miner.youtube_api import YouTubeAPI
from src.ai_brain.brain import AIBrain


class BackEndService:
    """
    Main backend service that orchestrates:
    1. YouTube data fetching
    2. AI analysis
    3. Communication with frontend
    """
    
    def __init__(self):
        self.youtube_api = YouTubeAPI()
        self.ai_brain = AIBrain()

    def fetch_and_process_video(self, url: str, max_comments: int = 50) -> Dict[str, Any]:
        """
        Fetch video data from YouTube API
        
        Args:
            url: YouTube video URL
            max_comments: Maximum number of comments to fetch
            
        Returns:
            Dictionary with video metadata and comments
        """
        try:
            video_record = self.youtube_api.process_video_link(url, max_comments=max_comments)
            return video_record
        except Exception as e:
            raise ValueError(f"Failed to fetch video data: {e}")

    def analyze_video_with_ai(self, video_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze video data using AI Brain
        
        Args:
            video_record: Video data from YouTube API
            
        Returns:
            Analysis results formatted for frontend
        """
        try:
            comments = video_record.get('comments', [])
            
            if not comments:
                return {
                    "analytics_data": {
                        "total_comments": 0,
                        "spam_count": 0,
                        "controversy_score": "N/A",
                        "sentiment_score": 0,
                        "top_topics": {"Topic": [], "Count": []}
                    },
                    "chat_seed": "This video has no comments yet."
                }
            
            # Batch analyze all comments
            batch_result = self.ai_brain.analyze_batch_comments(comments)
            
            if 'error' in batch_result:
                raise ValueError(f"AI analysis failed: {batch_result['error']}")
            
            # Extract aggregated data
            aggregated = batch_result.get('aggregated', {})
            avg_sentiment = aggregated.get('avg_sentiment', 0)
            avg_controversy = aggregated.get('avg_controversy', 0)
            theme_freq = aggregated.get('theme_frequency', {})
            
            # Format top topics for visualization
            sorted_themes = sorted(theme_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            top_topics = {
                "Topic": [theme for theme, _ in sorted_themes],
                "Count": [count for _, count in sorted_themes]
            }
            
            # Determine controversy level
            if avg_controversy < 3:
                controversy_label = "Low"
            elif avg_controversy < 7:
                controversy_label = "Medium"
            else:
                controversy_label = "High"
            
            # Count spam (simplified - using controversy as proxy)
            spam_count = sum(1 for analysis in batch_result.get('analyses', [])
                           if analysis.get('controversy_level', 0) > 8)
            
            # Generate insights
            insights = self.ai_brain.generate_insights(aggregated)
            
            # Format for frontend
            analytics_data = {
                "total_comments": len(comments),
                "spam_count": spam_count,
                "controversy_score": controversy_label,
                "sentiment_score": avg_sentiment,
                "top_topics": top_topics,
                "video_title": video_record.get('title', 'Unknown'),
                "channel": video_record.get('channel', 'Unknown'),
                "views": video_record.get('views', 0)
            }
            
            # Create chat seed message
            chat_seed = f"""I've analyzed {len(comments)} comments from "{video_record.get('title', 'this video')}".

**Key Findings:**
- Overall sentiment: {'Positive' if avg_sentiment > 0.3 else 'Negative' if avg_sentiment < -0.3 else 'Mixed'} ({avg_sentiment:.2f})
- Controversy level: {controversy_label}
- Top themes: {', '.join(top_topics['Topic'][:3]) if top_topics['Topic'] else 'None detected'}

Ask me anything about the audience feedback!"""
            
            return {
                "analytics_data": analytics_data,
                "chat_seed": chat_seed,
                "full_analysis": batch_result,
                "insights": insights
            }
            
        except Exception as e:
            raise ValueError(f"AI analysis failed: {e}")

    def communicate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send analysis to the Streamlit frontend by updating session state
        
        Args:
            analysis: Analysis results from analyze_video_with_ai
            
        Returns:
            Payload dict for confirmation
        """
        if analysis is None:
            raise ValueError("analysis is None")

        # Normalize: if analysis isn't wrapped, assume it's analytics_data
        if isinstance(analysis, dict) and "analytics_data" in analysis:
            analytics_data = analysis.get("analytics_data") or {}
            chat_seed = analysis.get("chat_seed")
            insights = analysis.get("insights")
        elif isinstance(analysis, dict):
            analytics_data = analysis
            chat_seed = None
            insights = None
        else:
            raise TypeError("analysis must be a dict")

        payload = {
            "type": "video_analysis",
            "status": "success",
            "analytics_data": analytics_data,
        }

        # Try to update Streamlit state if running in Streamlit
        try:
            import streamlit as st

            # Store the latest dashboard data
            st.session_state["analytics_data"] = analytics_data
            st.session_state["analysis_ready"] = True

            # Initialize or reset chat history
            initial_message = {
                "role": "assistant",
                "content": chat_seed or "Hello! I've analyzed the comments. Ask me anything about the audience sentiment or specific feedback."
            }
            
            st.session_state["messages"] = [initial_message]
            
            # Store full analysis for chat context
            st.session_state["full_analysis"] = analysis
            st.session_state["insights"] = insights

        except ModuleNotFoundError:
            # Not running in Streamlit; just return payload
            pass

        return payload

    def get_ai_chat_response(self, user_message: str) -> str:
        """
        Get a response from the AI chatbot
        
        Args:
            user_message: User's question
            
        Returns:
            AI's response
        """
        try:
            # Add context from analysis if available
            try:
                import streamlit as st
                full_analysis = st.session_state.get("full_analysis")
                
                if full_analysis:
                    # Provide context to the AI
                    context = f"""
You are analyzing a YouTube video with the following data:
- Total comments: {full_analysis.get('analytics_data', {}).get('total_comments', 0)}
- Average sentiment: {full_analysis.get('full_analysis', {}).get('aggregated', {}).get('avg_sentiment', 0):.2f}
- Top themes: {', '.join(full_analysis.get('analytics_data', {}).get('top_topics', {}).get('Topic', [])[:3])}

User question: {user_message}
"""
                    response = self.ai_brain.chat(context)
                else:
                    response = self.ai_brain.chat(user_message)
            except (ModuleNotFoundError, KeyError):
                # Fallback if not in Streamlit
                response = self.ai_brain.chat(user_message)
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"