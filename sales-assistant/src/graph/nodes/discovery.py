from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.graph.state import ConversationState
from src.prompts.base import CONTEXT_WINDOW
from src.prompts.discovery import DISCOVERY_SYSTEM_PROMPT
from src.utils.signals import extract_lead_signals

_llm = ChatOpenAI(
    model=settings.openai_model_default,
    temperature=0.4,
    api_key=settings.openai_api_key,
)


async def discovery_node(state: ConversationState) -> dict:
    profile = state.get("lead_profile", {})
    system = SystemMessage(
        content=DISCOVERY_SYSTEM_PROMPT.format(
            name=profile.get("name", ""),
            product_interest=profile.get("product_interest", ""),
        )
    )
    recent = state["messages"][-CONTEXT_WINDOW:]
    response = await _llm.ainvoke([system] + recent)

    # Extract any qualification signals from the latest human message
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )
    signals = extract_lead_signals(last_human)
    updated_profile = {**profile, **signals}

    return {
        "messages": [AIMessage(content=response.content)],
        "lead_profile": updated_profile,
        "current_stage": "qualifying",
        "turn_count": state.get("turn_count", 0) + 1,
    }


def route_from_discovery(state: ConversationState) -> str:
    if state.get("escalated"):
        return "escalation"
    profile = state.get("lead_profile", {})
    turn_count = state.get("turn_count", 0)
    max_turns = settings.max_discovery_turns

    has_interest = bool(profile.get("product_interest"))
    has_budget = bool(profile.get("budget_signal"))

    if has_interest and has_budget:
        return "recommendation"
    if turn_count >= max_turns:
        return "recommendation"
    return "discovery"
