# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- API ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# --- App ---
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "serene-secret-key")
APP_NAME = "Serene"
APP_URL = "http://localhost:5000"

# --- Model Parameters ---
TEMPERATURE = 0.75
MAX_TOKENS = 500

# --- Safety ---
MAX_HISTORY_LENGTH = 50