import json

from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.graph.state import ConversationState
from src.prompts.base import CONTEXT_WINDOW
from src.prompts.recommendation import RECOMMENDATION_SYSTEM_PROMPT
from src.services.catalog import get_cross_sell, products_to_json, search_products

_llm = ChatOpenAI(
    model=settings.openai_model_quality,
    temperature=0.5,
    api_key=settings.openai_api_key,
)


async def recommendation_node(state: ConversationState, db: AsyncSession) -> dict:
    profile = state.get("lead_profile", {})
    query = _build_search_query(profile)

    primary_products = await search_products(query, db, top_k=2)
    cross_sell = []
    if primary_products:
        cross_sell = await get_cross_sell(primary_products[0].product_id, db, top_k=1)

    all_products = primary_products + cross_sell
    products_json = products_to_json(all_products)

    primary_url = primary_products[0].purchase_url if primary_products else ""

    system = SystemMessage(
        content=RECOMMENDATION_SYSTEM_PROMPT.format(
            products_json=products_json,
            product_interest=profile.get("product_interest", ""),
            budget_signal=profile.get("budget_signal", "não informado"),
            preferences=_build_preferences(profile),
        )
    )
    recent = state["messages"][-CONTEXT_WINDOW:]
    response = await _llm.ainvoke([system] + recent)

    recommended_ids = [p.product_id for p in primary_products]

    return {
        "messages": [AIMessage(content=response.content)],
        "current_stage": "recommending",
        "products_recommended": state.get("products_recommended", []) + recommended_ids,
        "lead_profile": {
            **profile,
            "last_recommendation_url": primary_url,
        },
    }


def route_from_recommendation(state: ConversationState) -> str:
    if state.get("escalated"):
        return "escalation"
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    ).lower()
    objection_signals = ["caro", "caro", "não vou", "não quero", "medo", "espera", "pensar", "comparar"]
    if any(sig in last_human for sig in objection_signals):
        return "objection_handler"
    return "conversion"


def _build_search_query(profile: dict) -> str:
    parts = filter(None, [profile.get("product_interest"), profile.get("budget_signal")])
    return " ".join(parts) or "produto de beleza"


def _build_preferences(profile: dict) -> str:
    prefs = []
    interest = profile.get("product_interest", "")
    if "natural" in interest.lower():
        prefs.append("ingredientes naturais")
    if "vegano" in interest.lower():
        prefs.append("vegano")
    return ", ".join(prefs) if prefs else "não especificado"
