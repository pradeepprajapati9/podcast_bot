"""Faceless podcast bot: writes + voices one episode per run, publishes an
RSS feed on GitHub Pages. Submit the RSS to Spotify/Apple once; new episodes
then appear automatically. Run daily via GitHub Actions.
"""
import sys
import json
import os
import traceback
from datetime import datetime
from email.utils import formatdate

import config
import writer
import voiceover
import rss
import cover
import audio

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _load():
    if config.STATE_FILE.exists():
        try:
            return json.loads(config.STATE_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"episodes": []}


def _save(d):
    config.STATE_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), "utf-8")


def run():
    data = _load()
    used = [e["title"] for e in data["episodes"]]
    print(f"[podcast] {len(used)} episodes so far; creating a new one...")

    ep = writer.write_episode(used)
    if not ep:
        print("[podcast] could not generate an episode (Gemini issue).")
        return

    # monotonic, URL-safe slug (Hindi titles don't transliterate cleanly)
    count = data.get("count", 0) + 1
    data["count"] = count
    slug = f"ep{count}"
    ep["slug"] = slug

    # voice the body, then wrap with your recorded intro/outro if present (hybrid)
    mp3 = config.EPISODES_DIR / f"{slug}.mp3"
    body = config.EPISODES_DIR / f"{slug}_body.mp3"
    voiceover.make_audio(ep["script"], str(body))
    parts = ([str(config.INTRO)] if config.INTRO.exists() else []) + [str(body)] + \
            ([str(config.OUTRO)] if config.OUTRO.exists() else [])
    if len(parts) == 1:
        body.replace(mp3)
    else:
        audio.stitch(parts, str(mp3))
        body.unlink()
        print(f"[podcast] wrapped with {'intro' if config.INTRO.exists() else ''} "
              f"{'outro' if config.OUTRO.exists() else ''} (your voice)")

    words = len(ep["script"].split())
    entry = {
        "title": ep["title"], "slug": slug,
        "description": ep.get("description", ""),
        "bytes": os.path.getsize(mp3),
        "duration": int(words / 2.4),                 # ~rough seconds
        "pubDate": formatdate(localtime=False),       # RFC822 (UTC)
        "date": datetime.now().strftime("%d %b %Y"),
    }
    data["episodes"].append(entry)

    # cap repo size: keep only the most recent MAX_EPISODES (delete old mp3s)
    if len(data["episodes"]) > config.MAX_EPISODES:
        for old in data["episodes"][:-config.MAX_EPISODES]:
            f = config.EPISODES_DIR / f"{old['slug']}.mp3"
            try:
                f.unlink()
            except Exception:
                pass
        data["episodes"] = data["episodes"][-config.MAX_EPISODES:]

    ordered = list(reversed(data["episodes"]))        # newest first
    (config.DOCS_DIR / "feed.xml").write_text(rss.build_feed(ordered), "utf-8")
    (config.DOCS_DIR / "index.html").write_text(rss.build_index(ordered), "utf-8")
    cover.build()
    _save(data)

    print(f"[podcast] published: {ep['title']} ({entry['duration']}s)")
    print(f"[podcast] total episodes: {len(data['episodes'])}")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        print("ERROR:\n" + traceback.format_exc())
        sys.exit(1)
