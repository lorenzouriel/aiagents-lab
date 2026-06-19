import base64

import httpx
import structlog

from src.config import settings

log = structlog.get_logger()


class WhatsAppService:
    def __init__(self) -> None:
        self.base_url = settings.evolution_api_url
        self.instance = settings.evolution_instance_name
        self.headers = {
            "apikey": settings.evolution_api_key,
            "Content-Type": "application/json",
        }

    async def send_text(self, phone_number: str, text: str) -> dict:
        url = f"{self.base_url}/message/sendText/{self.instance}"
        payload = {"number": phone_number, "text": text}
        async with httpx.AsyncClient(timeout=15) as client:
            for attempt in range(3):
                try:
                    resp = await client.post(url, json=payload, headers=self.headers)
                    resp.raise_for_status()
                    return resp.json()
                except httpx.HTTPStatusError as exc:
                    if attempt == 2:
                        log.error("whatsapp_send_failed", phone=_mask(phone_number), status=exc.response.status_code)
                        raise
                    await _backoff(attempt)
        return {}

    async def download_audio_bytes(self, message_object: dict) -> bytes:
        url = f"{self.base_url}/chat/getBase64FromMediaMessage/{self.instance}"
        payload = {"message": message_object, "convertToMp4": False}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            return base64.b64decode(data["base64"])


def _mask(phone: str) -> str:
    return phone[:4] + "****" + phone[-4:] if len(phone) >= 8 else "****"


async def _backoff(attempt: int) -> None:
    import asyncio
    await asyncio.sleep(2 ** attempt)
