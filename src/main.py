# src/main.py
import sys
import os
import threading
import speech_recognition as sr
import pygame
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from ctypes import *
from dotenv import load_dotenv

# --- ERROR SUPPRESSION ---
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so.2')
asound.snd_lib_error_set_handler(c_error_handler)

# --- IMPORTS ---
from src.gui import KiraGUI
from src.brain import KiraBrain
from src.voice import KiraVoice
from src.skills import KiraSkills
from src.router import KiraRouter
from src.memory import KiraMemory  # <--- NEW
from src.tools import KiraTools    # <--- NEW

class WorkerSignals(QObject):
    update_state = pyqtSignal(str) 

class KiraController:
    def __init__(self):
        # GUI Setup
        self.app = QApplication(sys.argv)
        self.gui = KiraGUI()
        self.signals = WorkerSignals()
        self.signals.update_state.connect(self.gui.set_state)
        
        # Audio Init
        pygame.mixer.init()
        try:
            self.wake_sound = pygame.mixer.Sound("assets/sounds/wake.wav")
        except:
            self.wake_sound = None

        print("[System] Initializing Modules...")
        self.brain = KiraBrain()
        self.voice = KiraVoice()
        self.skills = KiraSkills()
        self.router = KiraRouter()
        
        # --- NEW AGENT MODULES ---
        self.memory = KiraMemory()
        self.tools = KiraTools()
        
        self.last_system_context = None 

        self.gui.show()
        self.listen_thread = threading.Thread(target=self.run_listening_loop, daemon=True)
        self.listen_thread.start()

    def execute_async(self, command):
        """Runs command in background"""
        def _run():
            result = self.skills.execute(f"[CMD: {command}]")
            self.last_system_context = f"Executed: {command}. Result: {result}"
            print(f"[Memory Updated] {self.last_system_context}")

        threading.Thread(target=_run, daemon=True).start()

    def run_listening_loop(self):
        r = sr.Recognizer()
        r.pause_threshold = 1.0  
        r.non_speaking_duration = 0.3
        
        WAKE_WORDS = ["kira", "khira", "kera", "kyra", "ciara", "kara"]

        try:
            mic = sr.Microphone(device_index=5, sample_rate=48000, chunk_size=4096)
        except:
            mic = sr.Microphone(sample_rate=48000, chunk_size=4096)

        with mic as source:
            print("[System] Calibrating...")
            r.adjust_for_ambient_noise(source, duration=0.5) 
            r.energy_threshold = 1500 
            
            print(f"[System] K.I.R.A. Online. (Wake Words: {WAKE_WORDS})")

            while True:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=None)
                    text = r.recognize_google(audio).lower()
                    print(f"\n[Heard]: {text}")
                    
                    if not any(alias in text for alias in WAKE_WORDS):
                        continue 

                    if self.wake_sound: self.wake_sound.play()
                    self.signals.update_state.emit("thinking")
                    
                    # --- 1. DEFINE LOCAL COMMANDS (CRITICAL FIX) ---
                    # This line MUST happen before 'if local_cmd:'
                    local_cmd, local_resp = self.router.check_intent(text)
                    
                    command_to_run = None
                    spoken_text = ""

                    # --- 2. CHECK FOR SPECIAL AGENT TOOLS ---
                    # Screen Reading check
                    if "read screen" in text or "what is on my screen" in text:
                        self.signals.update_state.emit("thinking")
                        screen_text = self.tools.read_screen()
                        self.last_system_context = f"SCREEN CONTENT: {screen_text}"
                        self.voice.speak("I've scanned your screen. What do you want to know?")
                        self.signals.update_state.emit("idle")
                        continue

                    # --- 3. MAIN LOGIC BRANCH ---
                    if local_cmd:
                        print("[FAST LANE] Local Intent Detected!")
                        spoken_text = local_resp
                        command_to_run = local_cmd
                    else:
                        print("[SLOW LANE] Thinking with Memory...")
                        
                        # A. Retrieve History
                        history = self.memory.get_context(limit=5)
                        
                        # B. Ask Brain
                        response_full = self.brain.ask(
                            text, 
                            context_injection=self.last_system_context,
                            history_context=history
                        )
                        self.last_system_context = None 
                        
                        # C. Save Memory
                        self.memory.save(text, response_full)
                        
                        spoken_text = response_full
                        if "[CMD:" in response_full:
                            parts = response_full.split("[CMD:")
                            spoken_text = parts[0].strip()
                            command_to_run = parts[1].split("]")[0].strip()

                    # --- 4. EXECUTION ---
                    print(f"Kira: {spoken_text}")
                    self.signals.update_state.emit("speaking")
                    self.voice.speak(spoken_text)
                    
                    if command_to_run:
                        if command_to_run in ["get_time", "check_status"]:
                             res = self.skills.execute(f"[CMD: {command_to_run}]")
                             if local_cmd: self.voice.speak(res)
                        else:
                            self.execute_async(command_to_run)

                    self.signals.update_state.emit("idle")
                    print("\nListening...")

                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"! Error: {e}")
                    self.signals.update_state.emit("idle")

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = KiraController()
    controller.run()