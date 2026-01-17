# --------------------------------------------------
# youtube_api.py
# --------------------------------------------------
import json
from typing import List, Dict, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class YouTubeAPI:
    """
    Wrapper class for interacting with YouTube data.
    Uses dummy_data.json for local development.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def load_dummy_data(self, path: str) -> List[Dict[str, Any]]:
        """Load mock YouTube API data."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def search_videos(self, query: str) -> List[Dict[str, Any]]:
        """
        Simulated YouTube search.
        In production, this would call the real YouTube Data API.
        """
        data = self.load_dummy_data("dummy_data.json")

        results = []
        for video in data:
            if query.lower() in video.get("title", "").lower():
                results.append(video)

        return results
