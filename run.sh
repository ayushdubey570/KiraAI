#!/bin/bash

# 1. Go to the project folder
cd /home/ayush/Desktop/KiraAI

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. CRITICAL FIX: Tell Python that the current folder (KiraAI) is the root
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 4. Run the AI
python -u src/main.py