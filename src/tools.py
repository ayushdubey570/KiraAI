# src/tools.py
import os
import pytesseract
from PIL import ImageGrab

class KiraTools:
    
    def save_file(self, filename, content):
        """
        Saves text to a file. 
        Example: save_file("/home/ayush/Desktop/note.txt", "Hello World")
        """
        try:
            # Security: Ensure we don't overwrite system files if possible, 
            # but for 'God Mode' we often allow it.
            with open(filename, "w") as f:
                f.write(content)
            return f"✅ Success: File saved to {filename}"
        except Exception as e:
            return f"❌ Error saving file: {e}"

    def read_screen(self):
        """
        Takes a screenshot and reads the text using Tesseract OCR.
        Returns the text found on screen.
        """
        try:
            print("[Tools] Taking screenshot...")
            # Capture the screen
            screenshot = ImageGrab.grab()
            
            print("[Tools] Reading text (OCR)...")
            # Extract text
            text = pytesseract.image_to_string(screenshot)
            
            if not text.strip():
                return "I scanned the screen, but it looks empty or has no readable text."
            
            # Return first 500 chars to avoid overwhelming the LLM
            return text.strip()[:1000] 
        except Exception as e:
            return f"Vision Error: {e}"