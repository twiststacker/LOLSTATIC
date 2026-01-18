import json
import os

CONFIG = {
    "RIOT_KEY": "RGAPI-1fe1ee95-ab41-4ba6-8b9d-6dfca2a40656",
    "OLLAMA_URL": "http://localhost:11434/api/generate",
    "OLLAMA_MODEL": "llama3.2",
    "OLLAMA_KEY": "84e219e983eb4a039ee047ae9785a81e.dUa-NVD-Ed6BUarpBnCFqLgK"
}

def load_config():
    """Loads settings.json if it exists, otherwise uses defaults."""
    try:
        if os.path.exists("settings.json") and os.path.getsize("settings.json") > 0:
            with open("settings.json", "r") as f:
                CONFIG.update(json.load(f))
    except Exception as e:
        print(f"⚠️ Config Load Error: {e}")
    return CONFIG
