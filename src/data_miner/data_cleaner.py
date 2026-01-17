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

    def _to_int(self, value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _clean_comments(self, comments: Any) -> List[str]:
        """
        Normalize comments to a list of cleaned strings.
        Accepts: list[str], str, None, or mixed lists.
        """
        if comments is None:
            return []

        # If a single string was provided, wrap it.
        if isinstance(comments, str):
            comments_list = [comments]
        # If it's a list/tuple, use it
        elif isinstance(comments, (list, tuple)):
            comments_list = list(comments)
        else:
            # Unknown type -> drop
            return []

        cleaned_comments: List[str] = []
        for c in comments_list:
            if c is None:
                continue
            # Convert non-strings to string (optional; you can also skip instead)
            if not isinstance(c, str):
                c = str(c)
            normalized = self.normalize_text(c)
            if normalized:  # drop empty after normalization
                cleaned_comments.append(normalized)

        return cleaned_comments

    def clean_youtube_data(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean and standardize YouTube API data.
        Expected fields: title, channel, views, published_at, comments
        """
        cleaned: List[Dict[str, Any]] = []

        for r in records:
            cleaned.append({
                "title": self.normalize_text(r.get("title", "")),
                "channel": self.normalize_text(r.get("channel", "")),
                "views": self._to_int(r.get("views", 0)),
                "published_at": r.get("published_at"),
                "comments": self._clean_comments(r.get("comments")),
            })

        return cleaned


