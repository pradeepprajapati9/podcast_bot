"""Generate a square podcast cover (1500x1500) - required by Spotify/Apple."""
from PIL import Image, ImageDraw, ImageFont
import config

S = 1500


def _font(size, bold=True):
    for p in ([r"C:\Windows\Fonts\Nirmala.ttc", r"C:\Windows\Fonts\arialbd.ttf"]):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def build():
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        t = y / S
        px_row = (int(99 * (1 - t) + 236 * t), int(102 * (1 - t) + 72 * t),
                  int(241 * (1 - t) + 153 * t))
        for x in range(S):
            px[x, y] = px_row
    d = ImageDraw.Draw(img)
    d.ellipse([S/2-150, 180, S/2+150, 480], outline="white", width=14)
    # mic glyph (simple)
    d.rounded_rectangle([S/2-45, 250, S/2+45, 400], radius=45, fill="white")
    tf = _font(120)
    y = 620
    for ln in _wrap(d, config.PODCAST_TITLE, tf, S - 200):
        w = d.textlength(ln, font=tf)
        d.text(((S - w) / 2, y), ln, font=tf, fill="white",
               stroke_width=3, stroke_fill=(0, 0, 0))
        y += 140
    sf = _font(54, bold=False)
    sub = "Daily Hindi Podcast" if config.POD_LANG == "hi" else "Daily Podcast"
    w = d.textlength(sub, font=sf)
    d.text(((S - w) / 2, y + 30), sub, font=sf, fill=(255, 240, 200))
    out = str(config.DOCS_DIR / "cover.jpg")
    img.convert("RGB").save(out, "JPEG", quality=88)
    return out


if __name__ == "__main__":
    print(build())
