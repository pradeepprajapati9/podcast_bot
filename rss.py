"""Build the podcast RSS feed (Spotify/Apple-compatible) + a simple web page."""
import html
import config

U = config.SITE_URL
ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def _esc(s):
    return html.escape(str(s or ""), quote=True)


def build_feed(episodes: list[dict]) -> str:
    chan = [
        f"<title>{_esc(config.PODCAST_TITLE)}</title>",
        f"<link>{U}/</link>",
        f"<language>{config.POD_LANG}</language>",
        f"<description>{_esc(config.PODCAST_DESC)}</description>",
        f"<itunes:author>{_esc(config.PODCAST_AUTHOR)}</itunes:author>",
        f"<itunes:summary>{_esc(config.PODCAST_DESC)}</itunes:summary>",
        f"<itunes:owner><itunes:name>{_esc(config.PODCAST_AUTHOR)}</itunes:name>"
        f"<itunes:email>{_esc(config.PODCAST_EMAIL)}</itunes:email></itunes:owner>",
        f'<itunes:image href="{U}/cover.jpg"/>',
        '<itunes:category text="Education"/>',
        "<itunes:explicit>no</itunes:explicit>",
        "<itunes:type>episodic</itunes:type>",
    ]
    items = []
    for e in episodes:                      # newest first (caller sorts)
        items.append(
            "<item>"
            f"<title>{_esc(e['title'])}</title>"
            f"<description>{_esc(e.get('description',''))}</description>"
            f"<itunes:summary>{_esc(e.get('description',''))}</itunes:summary>"
            f'<enclosure url="{U}/episodes/{e["slug"]}.mp3" length="{e.get("bytes",0)}" '
            f'type="audio/mpeg"/>'
            f'<guid isPermaLink="false">{e["slug"]}</guid>'
            f"<pubDate>{e.get('pubDate','')}</pubDate>"
            f"<itunes:duration>{e.get('duration',0)}</itunes:duration>"
            "<itunes:explicit>no</itunes:explicit></item>")
    return (f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<rss version="2.0" xmlns:itunes="{ITUNES}">'
            f'<channel>{"".join(chan)}{"".join(items)}</channel></rss>')


def build_index(episodes: list[dict]) -> str:
    cards = []
    for e in episodes:
        cards.append(
            f'<div class="card"><h3>{html.escape(e["title"])}</h3>'
            f'<p>{html.escape(e.get("description",""))}</p>'
            f'<audio controls preload="none" src="episodes/{e["slug"]}.mp3"></audio>'
            f'<p class="d">{e.get("date","")}</p></div>')
    css = ("body{margin:0;font-family:Segoe UI,system-ui,Arial,sans-serif;background:#f6f7fc;"
           "color:#1e2330;line-height:1.7}.wrap{max-width:760px;margin:0 auto;padding:0 18px}"
           "header{background:linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899);color:#fff;"
           "padding:30px 0;text-align:center}header img{width:160px;border-radius:18px;"
           "box-shadow:0 6px 20px rgba(0,0,0,.25)}.card{background:#fff;margin:16px 0;padding:20px;"
           "border-radius:14px;box-shadow:0 3px 14px rgba(30,35,48,.08)}.card h3{margin:.2em 0}"
           "audio{width:100%;margin-top:10px}.d{color:#6b7280;font-size:12px}a{color:#6366f1}")
    return (f'<!doctype html><html lang="{config.POD_LANG}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(config.PODCAST_TITLE)}</title>'
            f'<link rel="alternate" type="application/rss+xml" href="feed.xml">'
            f'<style>{css}</style></head><body>'
            f'<header><img src="cover.jpg" alt="cover"><h1>{html.escape(config.PODCAST_TITLE)}</h1>'
            f'<p>{html.escape(config.PODCAST_DESC)}</p>'
            f'<p><a href="feed.xml" style="color:#fff">RSS Feed</a></p></header>'
            f'<main class="wrap"><h2>Episodes</h2>{"".join(cards) or "<p>Coming soon...</p>"}'
            f'</main></body></html>')
