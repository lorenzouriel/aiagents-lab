from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.graph.state import ConversationState
from src.prompts.base import CONTEXT_WINDOW
from src.prompts.objection import OBJECTION_SYSTEM_PROMPT
from src.services.catalog import products_to_json, search_products

_llm = ChatOpenAI(
    model=settings.openai_model_quality,
    temperature=0.4,
    api_key=settings.openai_api_key,
)

_OBJECTION_KEYWORDS = {
    "price": ["caro", "muito", "preço", "barato", "desconto", "valor", "não tenho"],
    "delivery": ["demora", "prazo", "entrega", "rápido", "urgente"],
    "doubt": ["funciona", "qualidade", "certeza", "resultado", "confiança"],
    "competitor": ["outra loja", "concorrente", "comparando", "mais barato"],
}


async def objection_node(state: ConversationState, db: AsyncSession) -> dict:
    profile = state.get("lead_profile", {})
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    ).lower()

    objection_type = _detect_objection(last_human)
    recommended_ids = state.get("products_recommended", [])

    # Fetch alternative for price objections
    alternative_json = "[]"
    product_name = ""
    product_price = ""
    if objection_type == "price" and recommended_ids:
        query = profile.get("product_interest", "produto de beleza") + " barato"
        alts = await search_products(query, db, top_k=1)
        alternative_json = products_to_json(alts)

    system = SystemMessage(
        content=OBJECTION_SYSTEM_PROMPT.format(
            objection_type=objection_type,
            product_name=product_name,
            product_price=product_price,
            alternative_json=alternative_json,
            name=profile.get("name", ""),
        )
    )
    recent = state["messages"][-CONTEXT_WINDOW:]
    response = await _llm.ainvoke([system] + recent)

    objections = state.get("objections_raised", []) + [objection_type]

    return {
        "messages": [AIMessage(content=response.content)],
        "current_stage": "objecting",
        "objections_raised": objections,
    }


def route_from_objection(state: ConversationState) -> str:
    if state.get("escalated"):
        return "escalation"
    objections = state.get("objections_raised", [])
    # After 2 unresolved objections, escalate
    if len(objections) >= 2:
        return "escalation"
    return "conversion"


def _detect_objection(text: str) -> str:
    for obj_type, keywords in _OBJECTION_KEYWORDS.items():
        if any(k in text for k in keywords):
            return obj_type
    return "doubt"
