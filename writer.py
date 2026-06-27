"""Write one podcast episode (title, description, spoken script) with Gemini."""
import re
import json
import time
import requests
import config

MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]


def _gemini(prompt: str) -> str:
    if not config.GEMINI_API_KEY:
        return ""
    for attempt in range(2):
        for model in MODELS:
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{model}:generateContent?key={config.GEMINI_API_KEY}")
            try:
                r = requests.post(url, timeout=90,
                                  json={"contents": [{"parts": [{"text": prompt}]}]})
                if r.status_code == 200:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
                if r.status_code in (429, 503):
                    continue
            except Exception as ex:
                print(f"[writer] {model} error: {ex}")
        if attempt == 0:
            time.sleep(3)
    return ""


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60] or "episode"


def write_episode(used_titles: list[str]) -> dict | None:
    lang = "Hindi" if config.POD_LANG == "hi" else "English"
    avoid = "; ".join(used_titles[-60:]) or "none yet"
    prompt = (
        f"You are the host of a popular {lang} audio podcast about: {config.NICHE}.\n"
        f"Create ONE fresh, captivating episode. Do NOT repeat: {avoid}.\n"
        f"Return ONLY valid JSON, no markdown:\n"
        f'{{"title": "...", "description": "...", "script": "..."}}\n'
        f"Rules: title = catchy, curiosity-driving, in {lang}, under 70 chars. "
        f"description = 1-2 {lang} sentences for the episode notes. "
        f"script = a SPOKEN {lang} monologue of 380-520 words: open with a strong hook "
        f"that makes the listener stay, tell it like a friend (warm, simple, vivid), build "
        f"curiosity, and end by asking them to follow/subscribe for daily episodes. "
        f"Write the script as ONE continuous paragraph with NO line breaks. "
        f"Plain spoken text only - no markdown, no stage directions, no emojis, no headings."
    )
    raw = _gemini(prompt)
    if not raw:
        return None
    try:
        raw = raw[raw.find("{"): raw.rfind("}") + 1]
        raw = re.sub(r",\s*([}\]])", r"\1", raw)
        raw = re.sub(r"[\x00-\x1f]+", " ", raw)   # flatten newlines inside strings
        ep = json.loads(raw)
        if ep.get("title") and ep.get("script"):
            ep["slug"] = slugify(ep["title"])
            return ep
    except Exception as ex:
        print(f"[writer] parse failed: {ex}")
    return None
