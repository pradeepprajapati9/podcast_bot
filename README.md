# 🎙️ Faceless Podcast Bot (free, auto, Spotify/Apple)

Writes + voices one Hindi audio episode per run (Gemini + edge-tts) and publishes
an **RSS feed** on free GitHub Pages. Submit the RSS to Spotify/Apple **once** —
new episodes then appear automatically. Monetize via ads / sponsorships as it grows.

## How it works
```
pick topic -> Gemini writes a spoken script -> edge-tts -> episode.mp3 in /docs
-> rebuild RSS feed.xml + web page + cover -> GitHub Pages serves it
```

## Setup
1. Push to a GitHub repo named `podcast_bot` (Public).
2. **Settings -> Pages** -> Deploy from branch `main` `/docs`. Your feed:
   `https://<user>.github.io/podcast_bot/feed.xml`
3. Add Actions **secret** `GEMINI_API_KEY` and **variable** `SITE_URL`
   (= your Pages base URL, no trailing slash).
4. `.github/workflows/podcast.yml` then posts 1 episode/day.

## Submit to Spotify (one-time)
1. Go to https://podcasters.spotify.com -> Add your podcast -> **via RSS**.
2. Paste your feed URL (`.../podcast_bot/feed.xml`).
3. Verify (Spotify emails a code to PODCAST_EMAIL) -> submit.
   New episodes auto-appear on Spotify after that. (Apple Podcasts: same RSS.)

## Local test
```powershell
copy .env  # already has values; set GEMINI_API_KEY
pip install -r requirements.txt
python main.py   # writes one episode into /docs/episodes
```

Only the last `MAX_EPISODES` (60) audio files are kept to bound the repo.
