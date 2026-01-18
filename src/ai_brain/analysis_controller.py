from data_miner.youtube_api import YouTubeAPI
from brain import AIBrain

class BackEnd:
    def __init__(self):
        self.youtube_api = YouTubeAPI()
        self.ai_brain = AIBrain()

    def fetch_and_process_video(self, url):
        video_record = self.youtube_api.process_video_link(url, max_comments=500)
        return video_record
    
    def analyze_video_with_ai(self, video_record):
        analysis = self.ai_brain.analyze_video_data(video_record)
        return analysis
    
    # TODO: send analysis to front-end communicator when implemented
    def communicate_analysis(self, analysis):
        """
        Deliver analysis results to the frontend.

        Currently returns a structured payload.
        Future implementations may:
          - send over WebSocket
          - POST to frontend API
          - publish to message queue
        """
        if analysis is None:
            raise ValueError("Analysis payload is None")

        payload = {
            "type": "video_analysis",
            "status": "success",
            "data": analysis,
        }

        # Placeholder: return payload instead of sending
        return payload