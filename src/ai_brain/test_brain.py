import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

# --- TASK 1 & 4: THE CLIENT (The Engine) ---
class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.extraction_config = {
            "temperature": 0.1,  # Low for precision
            "response_mime_type": "application/json",
        }
        self.chat_config = {"temperature": 0.7} # High for personality

    def get_summarizer_model(self):
        system_prompt = "Return ONLY a JSON object with: 'sentiment_score' (float), 'top_3_themes' (list), and 'controversy_level' (int)."
        return genai.GenerativeModel("gemini-2.5-flash", generation_config=self.extraction_config, system_instruction=system_prompt)

# --- TASK 2: THE CHAT MANAGER (The Memory) ---
class ChatManager:
    def __init__(self, api_key, system_instruction):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)
        self.chat_session = self.model.start_chat(history=[])

    def send_message(self, user_text):
        try:
            response = self.chat_session.send_message(user_text)
            return response.text
        except Exception as e:
            return f"Error: {e}"

# --- TASK 3: EXECUTION & TESTING ---
if __name__ == "__main__":
    # Load API key from .env file
    MY_KEY = os.getenv("GEMINI_API_KEY")
    if not MY_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    print("--- Initializing The Brain ---")
    client = GeminiClient(MY_KEY)
    
    # Test Task 1: Summarization
    print("\n[Testing Task 1: Summarizer]")
    summarizer = client.get_summarizer_model()
    raw_data = "This video is great but the audio is quiet. I wish it was longer."
    summary = summarizer.generate_content(raw_data)
    print(f"Data Extracted: {summary.text}")

    # Test Task 2: Chatting
    print("\n[Testing Task 2: Chatbot]")
    bot = ChatManager(MY_KEY, "You are a helpful UBC Hackathon assistant.")
    print("User: Why should I use this tool?")
    print(f"AI: {bot.send_message('Why should I use this tool?')}")