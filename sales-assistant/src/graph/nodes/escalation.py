import structlog
from langchain_core.messages import AIMessage

from src.config import settings
from src.graph.state import ConversationState
from src.services.whatsapp import WhatsAppService

log = structlog.get_logger()
_wa = WhatsAppService()

_HANDOFF_MESSAGE = (
    "Entendido! Vou chamar um de nossos atendentes para te ajudar. "
    "Por favor, aguarde alguns instantes. 😊"
)

_OWNER_ALERT = (
    "🚨 *Escalação necessária*\n"
    "Cliente: {phone}\n"
    "Estágio: {stage}\n"
    "Última mensagem: {last_msg}"
)


async def escalation_node(state: ConversationState) -> dict:
    phone = state["phone_number"]
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )
    alert = _OWNER_ALERT.format(
        phone=phone,
        stage=state.get("current_stage", "unknown"),
        last_msg=last_human[:200],
    )

    try:
        await _wa.send_text(settings.owner_phone_number, alert)
    except Exception as exc:
        log.error("escalation_owner_alert_failed", error=str(exc))

    log.warning("lead_escalated", phone=phone[:4] + "****" + phone[-4:])

    return {
        "messages": [AIMessage(content=_HANDOFF_MESSAGE)],
        "current_stage": "escalated",
        "escalated": True,
    }
