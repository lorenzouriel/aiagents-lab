import pytest
from unittest.mock import AsyncMock, patch

from src.graph.nodes.discovery import discovery_node, route_from_discovery
from src.utils.signals import extract_lead_signals


@pytest.mark.asyncio
async def test_discovery_returns_ai_message(base_state):
    mock_response = AsyncMock()
    mock_response.content = "Para quem é o produto?"
    with patch("src.graph.nodes.discovery._llm.ainvoke", return_value=mock_response):
        result = await discovery_node(base_state)
    assert result["messages"][0].content == "Para quem é o produto?"
    assert result["current_stage"] == "qualifying"
    assert result["turn_count"] == 1


@pytest.mark.asyncio
async def test_discovery_extracts_name_from_message(base_state):
    from langchain_core.messages import HumanMessage
    base_state["messages"].append(HumanMessage(content="Me chamo Ana, quero hidratante"))
    mock_response = AsyncMock()
    mock_response.content = "Olá Ana!"
    with patch("src.graph.nodes.discovery._llm.ainvoke", return_value=mock_response):
        result = await discovery_node(base_state)
    assert result["lead_profile"].get("name") == "Ana"


def test_route_from_discovery_qualified(qualified_state):
    assert route_from_discovery(qualified_state) == "recommendation"


def test_route_from_discovery_not_qualified(base_state):
    base_state["turn_count"] = 1
    assert route_from_discovery(base_state) == "discovery"


def test_route_from_discovery_max_turns_forces_recommendation(base_state):
    base_state["turn_count"] = 3
    assert route_from_discovery(base_state) == "recommendation"


def test_route_from_discovery_escalated(base_state):
    base_state["escalated"] = True
    assert route_from_discovery(base_state) == "escalation"


@pytest.mark.parametrize("text,expected", [
    ("Tenho R$ 80 para gastar", {"budget_signal": "r$ 80"}),
    ("Preciso hoje urgente", {"urgency": "high"}),
    ("Sem pressa nenhuma", {"urgency": "low"}),
    ("Me chamo Maria", {"name": "Maria"}),
])
def test_extract_lead_signals(text, expected):
    signals = extract_lead_signals(text)
    for key, val in expected.items():
        assert signals.get(key) == val
