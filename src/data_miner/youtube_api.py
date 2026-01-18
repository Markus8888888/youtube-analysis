# --------------------------------------------------
# data_miner/youtube_api.py
# --------------------------------------------------
from __future__ import annotations

from typing import List, Dict, Any, Optional, Iterable


class YouTubeAPI:
    """
    Wrapper class for searching over YouTube-like data
    provided by the frontend (no file loading).

    Expected input: a list of dicts, each like:
      {
        "title": str,
        "channel": str,
        "views": int|str,
        "published_at": str|None,
        "comments": list[str] | str | None
      }
    """

    def __init__(self, initial_data: Optional[List[Dict[str, Any]]] = None):
        self._data: List[Dict[str, Any]] = []
        if initial_data is not None:
            self.set_data(initial_data)

    def set_data(self, data: List[Dict[str, Any]]) -> None:
        """Replace the internal dataset with data received from the frontend."""
        if not isinstance(data, list):
            raise TypeError("Frontend data must be a list of video dictionaries.")
        # Shallow validation (optional, but helpful)
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise TypeError(f"Video at index {i} is not a dict.")
        self._data = data

    def extend_data(self, data: List[Dict[str, Any]]) -> None:
        """Append additional videos to the internal dataset."""
        if not isinstance(data, list):
            raise TypeError("Frontend data must be a list of video dictionaries.")
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise TypeError(f"Video at index {i} is not a dict.")
        self._data.extend(data)

    def _normalize_text(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip().lower()

    def _normalize_comments(self, comments: Any) -> List[str]:
        """
        Normalize comments to a list[str].
        Accepts: list[str], str, None, or mixed lists.
        """
        if comments is None:
            return []
        if isinstance(comments, str):
            comments_list: Iterable[Any] = [comments]
        elif isinstance(comments, (list, tuple)):
            comments_list = comments
        else:
            return []

        out: List[str] = []
        for c in comments_list:
            txt = self._normalize_text(c)
            if txt:
                out.append(txt)
        return out

    def search_videos(
        self,
        query: str,
        data: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search videos by matching query primarily in comments,
        with title as a secondary signal.

        If `data` is provided, searches that list instead of internal stored data.
        """
        q = self._normalize_text(query)
        if not q:
            return []

        dataset = data if data is not None else self._data
        if not dataset:
            return []

        results: List[Dict[str, Any]] = []

        for video in dataset:
            title = self._normalize_text(video.get("title", ""))
            comments = self._normalize_comments(video.get("comments"))

            comment_match = any(q in c for c in comments)
            title_match = q in title

            if comment_match or title_match:
                results.append(video)

        return results
