"""
K.I.R.A. Source Package
Initializes the src directory as a Python package.
"""
def __init__(self):
        # ... existing code ...
        print("[System] Connecting to Neural Network...")
        self.brain = KiraBrain()
        self.voice = KiraVoice()
        self.skills = KiraSkills()  