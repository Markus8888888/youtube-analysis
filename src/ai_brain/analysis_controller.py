from typing import Any, Dict
from data_miner.youtube_link_processor import YouTubeAPI
from brain import AIBrain

class BackEndService:
    def __init__(self):
        self.youtube_api = YouTubeAPI()
        self.ai_brain = AIBrain()

    def fetch_and_process_video(self, url):
        video_record = self.youtube_api.process_video_link(url, max_comments=5)
        return video_record

    def analyze_video_with_ai(self, video_record):
        analysis = self.ai_brain.analyze_video_data(video_record)
        return analysis

    def communicate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends analysis to the Streamlit "frontend" by updating st.session_state.

        Expected analysis shape (recommended):
          {
            "analytics_data": {...},   # used by render_dashboard
            "chat_seed": "..."         # optional initial assistant message
          }

        If your AIBrain returns a single dict with keys like total_comments, sentiment_score, etc,
        we treat that dict as analytics_data.
        """
        if analysis is None:
            raise ValueError("analysis is None")

        # Normalize: if analysis isn't wrapped, assume it's analytics_data
        if isinstance(analysis, dict) and "analytics_data" in analysis:
            analytics_data = analysis.get("analytics_data") or {}
            chat_seed = analysis.get("chat_seed")
        elif isinstance(analysis, dict):
            analytics_data = analysis
            chat_seed = None
        else:
            raise TypeError("analysis must be a dict")

        payload = {
            "type": "video_analysis",
            "status": "success",
            "analytics_data": analytics_data,
        }

        # Try to update Streamlit state if running in Streamlit
        try:
            import streamlit as st  # type: ignore

            # Store the latest dashboard data
            st.session_state["analytics_data"] = analytics_data
            st.session_state["analysis_ready"] = True

            # Ensure chat history exists
            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {
                        "role": "assistant",
                        "content": "Hello! I've analyzed the comments. Ask me anything about the audience sentiment or specific feedback."
                    }
                ]

            # Optionally add a seed message summarizing analysis
            if chat_seed:
                st.session_state["messages"].append({"role": "assistant", "content": str(chat_seed)})

        except ModuleNotFoundError:
            # Not running Streamlit; just return payload
            pass

        return payload
