"""
YouTube API wrapper - combines link processor and data processor
"""
from src.data_miner.youtube_link_processor import YouTubeLinkProcessor
from src.data_miner.youtube_data_processor import YouTubeDataProcessor


class YouTubeAPI:
    """
    Main YouTube API interface
    Combines link processing and data management
    """
    
    def __init__(self):
        self.link_processor = YouTubeLinkProcessor()
        self.data_processor = YouTubeDataProcessor()

    #TODO: increase max_comments to 500 when the comment fetching is optimized
    def process_video_link(self, frontend_url, max_comments=5):
        """
        Process a YouTube URL and return video data with comments
        
        Args:
            frontend_url: YouTube video URL
            max_comments: Maximum number of comments to fetch (default: 50)
            
        Returns:
            Dictionary with video metadata and comments
        """
        record = self.link_processor.process_video_link(
            frontend_url, 
            max_comments=max_comments
        )
        self.data_processor.add_record(record)
        return record

    def search_videos(self, query):
        """
        Search through stored video data
        
        Args:
            query: Search query string
            
        Returns:
            List of matching video records
        """
        return self.data_processor.search_videos(query)