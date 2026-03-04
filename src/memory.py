# src/memory.py
import sqlite3
import datetime

class KiraMemory:
    def __init__(self, db_path="memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Creates the database table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                ai_response TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save(self, user_text, ai_text):
        """Saves a conversation pair."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO chat_history (timestamp, user_input, ai_response)
                VALUES (?, ?, ?)
            ''', (ts, user_text, ai_text))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[Memory Error] Could not save: {e}")

    def get_context(self, limit=5):
        """Retrieves the last 'limit' messages for context."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_input, ai_response FROM chat_history 
                ORDER BY id DESC LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            conn.close()
            
            # Format: Oldest -> Newest
            context_string = ""
            for user, ai in reversed(rows):
                context_string += f"User: {user}\nKira: {ai}\n"
            return context_string
        except Exception as e:
            print(f"[Memory Error] Could not read: {e}")
            return ""