import pytest
from unittest.mock import AsyncMock, patch

from src.graph.nodes.classifier import classifier_node, route_from_classifier
from src.graph.state import ConversationState


@pytest.mark.asyncio
@pytest.mark.parametrize("llm_output,expected_stage", [
    ("new_inquiry", "new_inquiry"),
    ("product_question", "product_question"),
    ("order_status", "order_status"),
    ("complaint", "complaint"),
    ("garbage_value", "new_inquiry"),  # fallback to new_inquiry
])
async def test_classifier_maps_intent(base_state, llm_output, expected_stage):
    mock_response = AsyncMock()
    mock_response.content = llm_output
    with patch("src.graph.nodes.classifier._llm.ainvoke", return_value=mock_response):
        result = await classifier_node(base_state)
    assert result["current_stage"] == expected_stage


def test_route_from_classifier_new_inquiry(base_state):
    base_state["current_stage"] = "new_inquiry"
    assert route_from_classifier(base_state) == "discovery"


def test_route_from_classifier_order_status(base_state):
    base_state["current_stage"] = "order_status"
    assert route_from_classifier(base_state) == "post_sale_support"


def test_route_from_classifier_complaint(base_state):
    base_state["current_stage"] = "complaint"
    assert route_from_classifier(base_state) == "escalation"


def test_route_from_classifier_product_question(base_state):
    base_state["current_stage"] = "product_question"
    assert route_from_classifier(base_state) == "recommendation"
