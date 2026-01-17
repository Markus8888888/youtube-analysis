# --------------------------------------------------
# data_miner/youtube_api.py
# --------------------------------------------------
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class YouTubeAPI:
    """
    Wrapper class for interacting with YouTube data.
    Uses dummy_data.json for local development.
    """

    def __init__(self, api_key: str | None = None, dummy_path: str | None = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        self.dummy_path = dummy_path

        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY is not set")

    def load_dummy_data(self, path: str) -> List[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def search_videos(self, query: str) -> List[Dict[str, Any]]:
        """
        Search videos by matching query primarily in comments,
        with title as a secondary signal.
        """
        q = (query or "").lower()
        data = self.load_dummy_data(self.dummy_path)

        results = []

        for video in data:
            comments = video.get("comments") or []
            title = video.get("title", "")

            comment_match = any(q in comment.lower() for comment in comments)
            title_match = q in title.lower()

            if comment_match or title_match:
                results.append(video)

        return results

    # def search_videos(self, query: str) -> List[Dict[str, Any]]:
    #     """
    #     Simulated YouTube search.
    #     In production, this would call the real YouTube Data API.
    #     """
    #     data = self.load_dummy_data("dummy_data.json")

    #     results = []
    #     for video in data:
    #         if query.lower() in video.get("title", "").lower():
    #             results.append(video)

    #     return results
