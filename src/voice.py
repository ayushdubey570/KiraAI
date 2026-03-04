# src/voice.py
import asyncio
import edge_tts
import pygame
import os

# --- VOICE SETTINGS ---
# VOICE: The specific persona.
# RATE: Speed. "+10%" is faster, "-10%" is slower.
# PITCH: Tone. "+5Hz" is higher (cuter), "-5Hz" is deeper.
VOICE = "ja-JP-NanamiNeural"  
RATE = "+6%"       
PITCH = "+10Hz"     

class KiraVoice:
    def __init__(self):
        self.output_file = "response.mp3"

    async def _generate_audio(self, text):
        """Generates audio with specific Rate and Pitch"""
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(self.output_file)

    def speak(self, text):
        try:
            # Run the async generation
            asyncio.run(self._generate_audio(text))
            
            # Play using Pygame
            pygame.mixer.init()
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Unload to release file lock
            pygame.mixer.music.unload()
            
        except Exception as e:
            print(f"[Voice Error] {e}")