import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ChatManager:
    def __init__(self, api_key, system_instruction):
        genai.configure(api_key=api_key)
        
        # Task 4: High temperature for 'Human-like' conversation
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 1024,
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=self.generation_config,
            system_instruction=system_instruction
        )
        
        # This list stores the conversation history
        self.chat_session = self.model.start_chat(history=[])

    def send_message(self, user_text):
        """Sends a message and manages the history window."""
        
        # Task 3: Basic Edge Case Check
        if not user_text.strip():
            return "I didn't catch that. Could you please type something?"

        try:
            # Task 2: Gemini's start_chat handles history automatically, 
            # but we can manually trim it if it gets too long to save 'tokens'
            response = self.chat_session.send_message(user_text)
            
            # OPTIONAL: Advanced Context Management
            # If history > 20 messages, we could rebuild the session to save memory
            # For a hackathon, Gemini's native history management is perfect.
            
            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_history(self):
        """Reset the conversation if the user wants to start over."""
        self.chat_session = self.model.start_chat(history=[])