"""Config for the faceless podcast bot."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"            # GitHub Pages root
EPISODES_DIR = DOCS_DIR / "episodes"    # mp3 files live here
ASSETS_DIR = BASE_DIR / "assets"        # your recorded intro/outro live here
STATE_FILE = BASE_DIR / "state.json"
EPISODES_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Your own-voice intro/outro (optional). Drop intro.* / outro.* in assets/ in ANY
# common format (mp3/m4a/wav/ogg - phone recordings work) and the bot wraps every
# AI-voiced episode with them (hybrid = your voice + automation).
def _find(name):
    for ext in ("mp3", "m4a", "mp4", "wav", "ogg", "aac", "amr", "opus"):
        p = ASSETS_DIR / f"{name}.{ext}"
        if p.exists():
            return p
    return ASSETS_DIR / f"{name}.mp3"   # default (may not exist yet)


INTRO = _find("intro")
OUTRO = _find("outro")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
SITE_URL = os.getenv("SITE_URL", "https://pradeepprajapati9.github.io/podcast_bot").rstrip("/")

PODCAST_TITLE = os.getenv("PODCAST_TITLE", "Gyaan Ki Baatein").strip()
PODCAST_AUTHOR = os.getenv("PODCAST_AUTHOR", "Pradeep Pk").strip()
PODCAST_DESC = os.getenv("PODCAST_DESC", "Roz ek dilchasp gyaan ki baat.").strip()
PODCAST_EMAIL = os.getenv("PODCAST_EMAIL", "you@example.com").strip()

POD_LANG = os.getenv("POD_LANG", "hi").lower()
VOICE = {"hi": "hi-IN-SwaraNeural", "en": "en-US-AvaMultilingualNeural"}.get(
    POD_LANG, "hi-IN-SwaraNeural")

# Keep the repo bounded: only the most recent N episodes are kept.
MAX_EPISODES = int(os.getenv("MAX_EPISODES", "60"))

# What the show is about (drives topic + script generation).
NICHE = os.getenv(
    "NICHE",
    "fascinating facts, true stories, psychology, science, history mysteries and "
    "motivational life lessons - told in simple, engaging Hindi for everyday Indian listeners",
)
