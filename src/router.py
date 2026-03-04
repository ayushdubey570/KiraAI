# src/router.py
import random

class KiraRouter:
    def __init__(self):
        # Define keywords that trigger local actions
        # Format: "keyword": ("command_id", [List of possible anime responses])
        self.intent_map = {
            "open terminal": ("open_terminal", ["Launch sequence initiated!", "Opening the terminal, Senpai.", "Terminal coming up!"]),
            "close terminal": ("close_terminal", ["Closing terminal now.", "Shutting it down!", "Bye bye terminal!"]),
            "open browser": ("open_browser", ["Opening the web for you.", "Browser launching!", "Here comes the internet!"]),
            "close browser": ("close_browser", ["Closing the browser.", "Browser closed, Master."]),
            "open files": ("open_files", ["Opening your files.", "File manager launching."]),
            "close files": ("close_files", ["Closing files.", "File manager closed."]),
            "open code": ("open_vscode", ["Opening VS Code.", "Time to code, Senpai!"]),
            "open vs code": ("open_vscode", ["Opening VS Code.", "Let's write some python!"]),
            "close code": ("close_vscode", ["Closing VS Code.", "Coding session over?"]),
            "what time": ("get_time", ["Checking the clock...", "Let me check the time."]),
            "system status": ("check_status", ["Scanning system vitals...", "Checking CPU and RAM."]),
        }

    def check_intent(self, user_text):
        """
        Returns (command, response_text) if a local match is found.
        Returns (None, None) if we should use Gemini.
        """
        text = user_text.lower()
        
        # Simple keyword matching
        for keyword, (command, responses) in self.intent_map.items():
            if keyword in text:
                # We found a match! Return the command and a random cute response
                return command, random.choice(responses)
        
        # No match found -> Send to Gemini
        return None, None