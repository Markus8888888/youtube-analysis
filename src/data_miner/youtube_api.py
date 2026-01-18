from .youtube_link_processor import YouTubeLinkProcessor
from .youtube_data_processor import YouTubeDataProcessor

class YouTubeAPI:
    def __init__(self):
        self.link_processor = YouTubeLinkProcessor()
        self.data_processor = YouTubeDataProcessor()

    def process_video_link(self, frontend_url, max_comments=50):
        record = self.link_processor.process_video_link(frontend_url, max_comments=max_comments)
        self.data_processor.add_record(record)
        return record

    def search_videos(self, query):
        return self.data_processor.search_videos(query)