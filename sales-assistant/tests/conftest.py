import pytest
from langchain_core.messages import AIMessage, HumanMessage
from unittest.mock import AsyncMock, MagicMock, patch

from src.graph.state import ConversationState


@pytest.fixture
def base_state() -> ConversationState:
    return ConversationState(
        messages=[HumanMessage(content="Oi, quero saber mais sobre vocês")],
        lead_id="test-lead-id",
        phone_number="5511999990001",
        current_stage="new",
        lead_profile={"phone_number": "5511999990001", "lead_id": "test-lead-id"},
        products_recommended=[],
        objections_raised=[],
        escalated=False,
        follow_up_scheduled=False,
        turn_count=0,
    )


@pytest.fixture
def qualified_state() -> ConversationState:
    return ConversationState(
        messages=[
            HumanMessage(content="Quero hidratante para pele oleosa"),
            AIMessage(content="Qual a sua faixa de investimento?"),
            HumanMessage(content="Tenho uns R$ 80 a R$ 100"),
        ],
        lead_id="test-lead-id",
        phone_number="5511999990001",
        current_stage="qualifying",
        lead_profile={
            "phone_number": "5511999990001",
            "lead_id": "test-lead-id",
            "product_interest": "hidratante para pele oleosa",
            "budget_signal": "R$ 80 a R$ 100",
            "urgency": "medium",
        },
        products_recommended=[],
        objections_raised=[],
        escalated=False,
        follow_up_scheduled=False,
        turn_count=2,
    )


@pytest.fixture
def mock_llm_response():
    """Factory fixture: returns a mock that yields a fixed content string."""
    def _factory(content: str):
        mock = AsyncMock()
        mock.content = content
        return mock
    return _factory
