# --------------------------------------------------
# data_miner/data_cleaner.py
# --------------------------------------------------
import json
from typing import List, Dict, Any


class DataCleaner:
    """
    Responsible for cleaning, normalizing, and validating
    raw data collected from external sources (e.g., APIs).
    """

    def __init__(self):
        pass

    def load_json(self, path: str) -> List[Dict[str, Any]]:
        """Load raw JSON data from a file."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def remove_nulls(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove keys with null values."""
        cleaned = []
        for r in records:
            cleaned.append({k: v for k, v in r.items() if v is not None})
        return cleaned

    def normalize_text(self, text: str) -> str:
        """Basic text normalization."""
        return text.strip().lower()

    def clean_youtube_data(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean and standardize YouTube API data.
        Expected fields: title, channel, views, published_at
        """
        cleaned = []

        for r in records:
            cleaned.append({
                "title": self.normalize_text(r.get("title", "")),
                "channel": self.normalize_text(r.get("channel", "")),
                "views": int(r.get("views", 0)),
                "published_at": r.get("published_at"),
            })

        return cleaned


