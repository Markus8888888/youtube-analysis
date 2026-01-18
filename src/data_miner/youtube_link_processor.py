# --------------------------------------------------
# data_miner/youtube_api.py
# --------------------------------------------------
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import parse_qs, urlparse

import requests


# -----------------------------
# Link processing / API fetching
# -----------------------------
@dataclass(frozen=True)
class YouTubeVideoRecord:
    video_id: str
    title: str
    channel: str
    views: int
    published_at: Optional[str]
    comments: List[str]


class YouTubeLinkProcessor:
    """
    Responsible for:
      - parsing YouTube URLs -> video_id
      - fetching video metadata + (optional) comments via YouTube Data API v3
      - returning a normalized record ()
    """
    
    #streamlit run app.py
    YT_API_BASE = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: Optional[str] = None, session: Optional[requests.Session] = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY is not set (required to fetch data from YouTube).")
        self.session = session or requests.Session()

    def process_video_link(
        self,
        url: str,
        *,
        max_comments: int = 100,
        include_comments: bool = True,
        timeout: float = 15.0,
    ) -> Dict[str, Any]:
        """
        Given a YouTube link, return a normalized dict record.

        Output shape:
          {
            "video_id": "...",
            "title": "...",
            "channel": "...",
            "views": 123,
            "published_at": "...",
            "comments": ["...", ...]
          }
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract YouTube video id from url: {url}")

        details = self.fetch_video_details(video_id, timeout=timeout)
        if not details:
            raise ValueError(f"No video found for id: {video_id}")

        comments: List[str] = []
        if include_comments and max_comments > 0:
            comments = self.fetch_top_level_comments(video_id, max_results=max_comments, timeout=timeout)

        record = YouTubeVideoRecord(
            video_id=video_id,
            title=details["title"],
            channel=details["channel"],
            views=details["views"],
            published_at=details.get("published_at"),
            comments=comments,
        )

        # Return as plain dict for easy JSON serialization
        return {
            "video_id": record.video_id,
            "title": record.title,
            "channel": record.channel,
            "views": record.views,
            "published_at": record.published_at,
            "comments": record.comments,
        }

    def extract_video_id(self, url: str) -> Optional[str]:
        if not url or not isinstance(url, str):
            return None

        url = url.strip()
        parsed = urlparse(url)
        host = (parsed.netloc or "").lower()
        path = parsed.path or ""

        is_youtube = (
            host == "youtu.be"
            or host.endswith(".youtu.be")
            or host == "youtube.com"
            or host.endswith(".youtube.com")
            or host == "m.youtube.com"
            or host == "www.youtube.com"
        )

        # Only accept known YouTube hosts
        if not is_youtube:
            return None

        # youtu.be/VIDEOID
        if "youtu.be" in host:
            vid = path.strip("/").split("/")[0]
            return vid or None

        # youtube.com/watch?v=VIDEOID
        qs = parse_qs(parsed.query or "")
        if "v" in qs and qs["v"]:
            return qs["v"][0]

        # youtube.com/shorts/VIDEOID or /embed/VIDEOID
        m = re.match(r"^/(shorts|embed)/([^/?#]+)", path)
        if m:
            return m.group(2)

        return None

    def fetch_video_details(self, video_id: str, *, timeout: float = 15.0) -> Optional[Dict[str, Any]]:
        """
        videos.list?part=snippet,statistics&id=...
        """
        endpoint = f"{self.YT_API_BASE}/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": self.api_key,
        }

        r = self.session.get(endpoint, params=params, timeout=timeout)
        r.raise_for_status()
        payload = r.json()

        items = payload.get("items") or []
        if not items:
            return None

        item = items[0]
        snippet = item.get("snippet") or {}
        stats = item.get("statistics") or {}

        title = snippet.get("title") or ""
        channel = snippet.get("channelTitle") or ""
        published_at = snippet.get("publishedAt")
        view_count_raw = stats.get("viewCount")

        try:
            views = int(view_count_raw) if view_count_raw is not None else 0
        except (TypeError, ValueError):
            views = 0

        return {
            "title": title,
            "channel": channel,
            "published_at": published_at,
            "views": views,
        }

    def fetch_top_level_comments(
        self,
        video_id: str,
        *,
        max_results: int = 100,
        timeout: float = 15.0,
    ) -> List[str]:
        """
        commentThreads.list?part=snippet&videoId=...
        Top-level comments only.
        """
        endpoint = f"{self.YT_API_BASE}/commentThreads"
        comments: List[str] = []

        page_token: Optional[str] = None
        remaining = max(0, max_results)

        while remaining > 0:
            batch_size = min(100, remaining)
            params = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": batch_size,
                "textFormat": "plainText",
                "key": self.api_key,
            }
            if page_token:
                params["pageToken"] = page_token

            r = self.session.get(endpoint, params=params, timeout=timeout)
            # comments can be disabled; commonly returns 403
            if r.status_code == 403:
                return comments
            r.raise_for_status()

            payload = r.json()
            items = payload.get("items") or []

            for it in items:
                sn = (((it.get("snippet") or {}).get("topLevelComment") or {}).get("snippet") or {})
                text = sn.get("textDisplay") or sn.get("textOriginal") or ""
                text = str(text).strip()
                if text:
                    comments.append(text)

            remaining = max_results - len(comments)
            page_token = payload.get("nextPageToken")
            if not page_token or not items:
                break

        return comments
