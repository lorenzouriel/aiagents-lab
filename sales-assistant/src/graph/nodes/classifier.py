from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.graph.state import ConversationState
from src.prompts.base import CONTEXT_WINDOW
from src.prompts.classifier import CLASSIFIER_SYSTEM_PROMPT

_llm = ChatOpenAI(
    model=settings.openai_model_default,
    temperature=0,
    api_key=settings.openai_api_key,
)

_VALID_INTENTS = {
    "new_inquiry",
    "product_question",
    "order_status",
    "complaint",
    "follow_up_response",
    "resume",
}


async def classifier_node(state: ConversationState) -> dict:
    recent = state["messages"][-CONTEXT_WINDOW:]
    response = await _llm.ainvoke(
        [SystemMessage(content=CLASSIFIER_SYSTEM_PROMPT)] + recent
    )
    intent = response.content.strip().lower()

    if intent not in _VALID_INTENTS:
        intent = "new_inquiry"

    return {"current_stage": intent}


def route_from_classifier(state: ConversationState) -> str:
    stage = state.get("current_stage", "new_inquiry")
    routing = {
        "new_inquiry": "discovery",
        "product_question": "recommendation",
        "order_status": "post_sale_support",
        "complaint": "escalation",
        "follow_up_response": "discovery",
        "resume": "discovery",
    }
    return routing.get(stage, "discovery")
