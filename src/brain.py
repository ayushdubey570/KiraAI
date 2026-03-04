# src/brain.py
import google.generativeai as genai
from src.config import API_KEY, SYSTEM_PROMPT

class KiraBrain:
    def __init__(self):
        genai.configure(api_key=API_KEY)
        # We use flash for speed and cost effectiveness
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def ask(self, user_text, context_injection=None, history_context=None):
        """
        user_text: What you said now.
        context_injection: System status/Last command result (Short term).
        history_context: Database memory of past chats (Long term).
        """
        
        # Build the Ultimate Prompt
        full_prompt = f"""
{SYSTEM_PROMPT}

[MEMORY - PAST CONVERSATION]
{history_context if history_context else "No previous memory."}

[SYSTEM STATUS / ACTION RESULTS]
{context_injection if context_injection else "No system updates."}

[CURRENT USER INPUT]
User: {user_text}
Kira:
"""
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Brain Error: {e}"