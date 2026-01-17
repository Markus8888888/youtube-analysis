import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        
        # TASK 4: Define different 'personalities' for the model
        # 1. Precise & Robotic for Data Extraction (JSON)
        self.extraction_config = {
            "temperature": 0.1,  # Low = No creativity, high accuracy
            "top_p": 0.95,
            "response_mime_type": "application/json", # Forces JSON output
        }
        
        # 2. Creative & Helpful for the Chatbot
        self.chat_config = {
            "temperature": 0.7,  # High = More "human" and varied
            "top_p": 0.95,
        }

    def get_summarizer_model(self):
        """Task 1: Setup for the JSON Summarizer"""
        system_prompt = (
            "You are a data extraction tool. Analyze YouTube comments and return "
            "ONLY a JSON object with: 'sentiment_score' (float -1 to 1), "
            "'top_3_themes' (list), and 'controversy_level' (int 1-10)."
        )
        return genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=self.extraction_config,
            system_instruction=system_prompt
        )

    def get_chat_model(self, system_instruction):
        """Task 2 & 4: Setup for the Chatbot"""
        return genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=self.chat_config,
            system_instruction=system_instruction
        )

    def safe_generate_content(self, model, prompt):
        """Task 3: Testing & Error Handling (The "Safety Net")"""
        if not prompt or len(prompt.strip()) == 0:
            return None
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"API Error: {e}")
            return None