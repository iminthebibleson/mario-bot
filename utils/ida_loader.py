import json
from pathlib import Path

DATA_DIR = Path("data")

def load_sprites():
    with open(DATA_DIR / "sprites.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_profiles():
    with open(DATA_DIR / "profiles.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_xrefs():
    try:
        with open(DATA_DIR / "xrefs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}