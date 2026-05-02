import os
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama3.1:8b"
OLLAMA_HOST = "http://localhost:11434"
MAX_STEPS = 5