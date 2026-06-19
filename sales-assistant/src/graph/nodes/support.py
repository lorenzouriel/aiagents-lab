import json
import re

from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.graph.state import ConversationState
from src.prompts.base import CONTEXT_WINDOW
from src.prompts.support import SUPPORT_SYSTEM_PROMPT
from src.services.nuvemshop import fetch_order

_llm = ChatOpenAI(
    model=settings.openai_model_default,
    temperature=0.3,
    api_key=settings.openai_api_key,
)

_ESCALATE_SIGNALS = ["produto errado", "avariado", "danificado", "troca", "devolução", "reembolso"]


async def support_node(state: ConversationState) -> dict:
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )

    if any(sig in last_human.lower() for sig in _ESCALATE_SIGNALS):
        return {"escalated": True, "current_stage": "escalation"}

    order_number = _extract_order_number(last_human)
    order_data: dict | None = None
    if order_number:
        order_data = await fetch_order(order_number)

    order_json = json.dumps(order_data, ensure_ascii=False) if order_data else "null"

    system = SystemMessage(
        content=SUPPORT_SYSTEM_PROMPT.format(order_json=order_json)
    )
    recent = state["messages"][-CONTEXT_WINDOW:]
    response = await _llm.ainvoke([system] + recent)

    return {
        "messages": [AIMessage(content=response.content)],
        "current_stage": "support",
    }


def route_from_support(state: ConversationState) -> str:
    if state.get("escalated"):
        return "escalation"
    return "__end__"


def _extract_order_number(text: str) -> str | None:
    match = re.search(r"#?\s*(\d{4,})", text)
    return match.group(1) if match else None
