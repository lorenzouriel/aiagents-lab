import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.graph.nodes.recommendation import (
    _build_search_query,
    _build_preferences,
    route_from_recommendation,
)
from langchain_core.messages import HumanMessage


def test_build_search_query_with_interest_and_budget(qualified_state):
    query = _build_search_query(qualified_state["lead_profile"])
    assert "hidratante" in query
    assert "R$" in query or "80" in query


def test_build_search_query_fallback():
    assert _build_search_query({}) == "produto de beleza"


def test_build_preferences_natural():
    prefs = _build_preferences({"product_interest": "hidratante natural vegano"})
    assert "ingredientes naturais" in prefs
    assert "vegano" in prefs


def test_build_preferences_none():
    prefs = _build_preferences({})
    assert prefs == "não especificado"


def test_route_from_recommendation_to_conversion(qualified_state):
    qualified_state["messages"].append(HumanMessage(content="Adorei! Como faço o pedido?"))
    assert route_from_recommendation(qualified_state) == "conversion"


def test_route_from_recommendation_to_objection_on_price(qualified_state):
    qualified_state["messages"].append(HumanMessage(content="Achei caro, tem algo mais barato?"))
    assert route_from_recommendation(qualified_state) == "objection_handler"


def test_route_from_recommendation_escalation_flag(qualified_state):
    qualified_state["escalated"] = True
    assert route_from_recommendation(qualified_state) == "escalation"
