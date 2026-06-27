"""Stitch audio parts (your intro + AI body + your outro) into one mp3 via ffmpeg.
Re-encodes so different sample rates/formats join cleanly."""
import subprocess
import imageio_ffmpeg


def stitch(parts: list[str], out_path: str):
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    inputs = []
    for p in parts:
        inputs += ["-i", p]
    n = len(parts)
    filt = "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    cmd = ([ff, "-y"] + inputs +
           ["-filter_complex", filt, "-map", "[a]",
            "-c:a", "libmp3lame", "-b:a", "96k", "-ar", "24000", out_path])
    subprocess.run(cmd, check=True, capture_output=True)
