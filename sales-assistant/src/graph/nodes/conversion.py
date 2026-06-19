from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.graph.state import ConversationState
from src.prompts.base import CONTEXT_WINDOW
from src.prompts.conversion import CONVERSION_SYSTEM_PROMPT
from src.services.kestra import KestraClient
from src.utils.scoring import compute_temperature

_llm = ChatOpenAI(
    model=settings.openai_model_default,
    temperature=0.4,
    api_key=settings.openai_api_key,
)
_kestra = KestraClient()

_FRUSTRATION_KEYWORDS = ["absurdo", "ridículo", "péssimo", "horrível", "nunca mais", "mentira"]


async def conversion_node(state: ConversationState) -> dict:
    profile = state.get("lead_profile", {})
    purchase_url = profile.get("last_recommendation_url", "https://vaib2.lojavirtualnuvem.com.br/")

    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    ).lower()

    if any(k in last_human for k in _FRUSTRATION_KEYWORDS):
        return {"escalated": True, "current_stage": "escalation"}

    products_summary = ", ".join(state.get("products_recommended", [])[:2]) or "produtos selecionados"

    system = SystemMessage(
        content=CONVERSION_SYSTEM_PROMPT.format(
            products_summary=products_summary,
            purchase_url=purchase_url,
        )
    )
    recent = state["messages"][-CONTEXT_WINDOW:]
    response = await _llm.ainvoke([system] + recent)

    temperature = compute_temperature(state)

    # Schedule 24h follow-up if link was sent and customer didn't confirm purchase
    await _kestra.trigger_followup(state["phone_number"], delay_hours=24)

    return {
        "messages": [AIMessage(content=response.content)],
        "current_stage": "converting",
        "follow_up_scheduled": True,
        "lead_profile": {**profile, "temperature": temperature},
    }


def route_from_conversion(state: ConversationState) -> str:
    if state.get("escalated"):
        return "escalation"
    return "__end__"
