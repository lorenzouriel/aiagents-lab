import io

import structlog
from openai import AsyncOpenAI

from src.config import settings

log = structlog.get_logger()
_openai = AsyncOpenAI(api_key=settings.openai_api_key)


async def transcribe_audio(audio_bytes: bytes, mime_type: str = "audio/ogg") -> str:
    ext = mime_type.split("/")[-1].split(";")[0].strip()
    filename = f"audio.{ext}"
    file_obj = io.BytesIO(audio_bytes)
    file_obj.name = filename

    response = await _openai.audio.transcriptions.create(
        model="whisper-1",
        file=(filename, file_obj, mime_type),
        language="pt",
    )
    log.info("whisper_transcribed", chars=len(response.text))
    return response.text
