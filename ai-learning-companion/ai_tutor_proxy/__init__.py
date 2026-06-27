# Init
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "provider_config.local.json")
if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data = json.load(f)
            for k, v in config_data.items():
                if v and v not in ("your_gemini_key_here", "your_openai_or_openrouter_key_here"):
                    os.environ[k] = v
    except Exception:
        pass
