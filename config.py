from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY") or os.getenv("COHERE-API-KEY")

if not COHERE_API_KEY:
    raise ValueError(f"COHERE_API_KEY not found in .env. Found keys: {[k for k in os.environ if 'COHERE' in k]}")
