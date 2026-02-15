"""YouTube Data API v3 client for competitive analysis."""

from typing import List, Dict, Any, Optional, Tuple
from loguru import logger

from config.settings import YOUTUBE_API_KEY, YOUTUBE_MAX_RESULTS


class YouTubeService:
    """Handles YouTube Data API interactions for competitive analysis."""

    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
        self._client = None

    @property
    def client(self):
        if self._client is None and self.api_key:
            from googleapiclient.discovery import build
            self._client = build("youtube", "v3", developerKey=self.api_key)
        return self._client

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def search_videos(self, query: str, max_results: int = YOUTUBE_MAX_RESULTS) -> List[Dict[str, Any]]:
        """Search YouTube for videos on a topic."""
        if not self.is_configured():
            return []

        try:
            search_response = self.client.search().list(
                q=query,
                part="id,snippet",
                type="video",
                order="relevance",
                maxResults=min(max_results, 50),
            ).execute()

            video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
            if not video_ids:
                return []

            # Get detailed video statistics
            videos_response = self.client.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(video_ids),
            ).execute()

            results = []
            for video in videos_response.get("items", []):
                snippet = video["snippet"]
                stats = video.get("statistics", {})
                results.append({
                    "video_id": video["id"],
                    "title": snippet.get("title", ""),
                    "channel": snippet.get("channelTitle", ""),
                    "description": snippet.get("description", "")[:500],
                    "published_at": snippet.get("publishedAt", ""),
                    "tags": snippet.get("tags", []),
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "duration": video.get("contentDetails", {}).get("duration", ""),
                })

            # Sort by views
            results.sort(key=lambda x: x["views"], reverse=True)
            return results

        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return []

    def format_for_analysis(self, videos: List[Dict[str, Any]]) -> str:
        """Format video data for Gemini analysis prompt."""
        if not videos:
            return "No YouTube data available."

        lines = [f"=== TOP {len(videos)} COMPETING VIDEOS ===\n"]
        for i, v in enumerate(videos, 1):
            tags_str = ", ".join(v.get("tags", [])[:10]) if v.get("tags") else "None"
            lines.append(f"""
Video #{i}:
  Title: {v['title']}
  Channel: {v['channel']}
  Views: {v['views']:,}
  Likes: {v['likes']:,}
  Comments: {v['comments']:,}
  Tags: {tags_str}
  Published: {v['published_at'][:10] if v['published_at'] else 'Unknown'}
""")
        return "\n".join(lines)

    def get_tag_analysis(self, videos: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze common tags across competing videos."""
        tag_counts: Dict[str, int] = {}
        for video in videos:
            for tag in video.get("tags", []):
                tag_lower = tag.lower()
                tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))

    def test_connection(self) -> Tuple[bool, str]:
        """Test the YouTube API connection."""
        try:
            response = self.client.search().list(
                q="test",
                part="id",
                type="video",
                maxResults=1,
            ).execute()
            return True, f"Connected. Quota used for test search."
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
