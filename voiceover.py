"""Text -> MP3 episode audio using edge-tts (free neural voices)."""
import asyncio
import edge_tts
import config


async def _synth(text: str, out_path: str):
    await edge_tts.Communicate(text, config.VOICE).save(out_path)


def make_audio(text: str, out_path: str) -> str:
    asyncio.run(_synth(text, out_path))
    return out_path
