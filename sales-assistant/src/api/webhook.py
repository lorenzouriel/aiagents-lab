import structlog
from fastapi import APIRouter, BackgroundTasks, Request
from langchain_core.messages import HumanMessage

from src.db.postgres import AsyncSessionFactory
from src.db.redis import get_redis
from src.graph.builder import get_compiled_graph
from src.graph.state import ConversationState
from src.services.memory import get_or_create_lead, update_lead
from src.services.whatsapp import WhatsAppService
from src.services.whisper import transcribe_audio

log = structlog.get_logger()
router = APIRouter()
_wa = WhatsAppService()


@router.post("/webhook/evolution")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    if payload.get("event") != "messages.upsert":
        return {"status": "ignored"}

    data = payload.get("data", {})
    if data.get("key", {}).get("fromMe"):
        return {"status": "ignored"}

    phone = data["key"]["remoteJid"].replace("@s.whatsapp.net", "")
    msg_id = data["key"].get("id", "")
    msg_type = data.get("messageType", "")

    if msg_type not in ("conversation", "extendedTextMessage", "audioMessage"):
        return {"status": "unsupported_type"}

    background_tasks.add_task(_process, payload, phone, msg_id, msg_type, data)
    return {"status": "received"}


@router.post("/internal/followup")
async def trigger_followup(request: Request):
    """Called by Kestra to deliver scheduled follow-up messages."""
    body = await request.json()
    phone = body.get("phone_number")
    message = body.get("message", "Oi! Ainda posso te ajudar com algo? 😊")
    if phone:
        await _wa.send_text(phone, message)
    return {"status": "sent"}


async def _process(payload: dict, phone: str, msg_id: str, msg_type: str, data: dict) -> None:
    redis = await get_redis()
    lock_key = f"processing:{msg_id}"

    if not await redis.set(lock_key, "1", ex=60, nx=True):
        return  # duplicate delivery

    try:
        text = await _extract_text(msg_type, data)
        if not text:
            return

        async with AsyncSessionFactory() as db:
            lead = await get_or_create_lead(phone, db)
            lead_id = str(lead.lead_id)

        graph = get_compiled_graph()
        config = {"configurable": {"thread_id": phone}}

        initial_state: dict = {
            "messages": [HumanMessage(content=text)],
            "phone_number": phone,
            "lead_id": lead_id,
            "lead_profile": {"phone_number": phone, "lead_id": lead_id},
            "products_recommended": [],
            "objections_raised": [],
            "escalated": False,
            "follow_up_scheduled": False,
            "turn_count": 0,
            "current_stage": "new",
        }

        result = await graph.ainvoke(initial_state, config=config)

        # Send the last AI message back to WhatsApp
        ai_reply = next(
            (m.content for m in reversed(result["messages"]) if m.type == "ai"),
            None,
        )
        if ai_reply:
            await _wa.send_text(phone, ai_reply)

        # Persist lead state updates
        async with AsyncSessionFactory() as db:
            profile = result.get("lead_profile", {})
            await update_lead(
                phone,
                db,
                lead_stage=result.get("current_stage", "new"),
                lead_temperature=profile.get("temperature", "cold"),
                budget_signal=profile.get("budget_signal"),
                product_interest=profile.get("product_interest"),
                urgency=profile.get("urgency"),
                name=profile.get("name"),
                escalated=result.get("escalated", False),
                follow_up_scheduled=result.get("follow_up_scheduled", False),
            )

    except Exception as exc:
        log.error("message_processing_failed", phone=phone[:6] + "****", error=str(exc))


async def _extract_text(msg_type: str, data: dict) -> str:
    message = data.get("message", {})
    if msg_type == "conversation":
        return message.get("conversation", "")
    if msg_type == "extendedTextMessage":
        return message.get("extendedTextMessage", {}).get("text", "")
    if msg_type == "audioMessage":
        audio_msg = message.get("audioMessage", {})
        audio_bytes = await _wa.download_audio_bytes(data.get("message", {}))
        mime = audio_msg.get("mimetype", "audio/ogg")
        return await transcribe_audio(audio_bytes, mime_type=mime)
    return ""
