import pytest

from src.graph.nodes.objection import _detect_objection, route_from_objection


@pytest.mark.parametrize("text,expected_type", [
    ("tá muito caro pra mim", "price"),
    ("quero desconto", "price"),
    ("demora muito para entrega", "delivery"),
    ("prazo de entrega é longo", "delivery"),
    ("será que funciona mesmo?", "doubt"),
    ("vi na outra loja mais barato", "competitor"),
    ("só quero pensar um pouco", "doubt"),  # fallback
])
def test_detect_objection(text, expected_type):
    assert _detect_objection(text.lower()) == expected_type


def test_route_from_objection_single_escalates_to_conversion(qualified_state):
    qualified_state["objections_raised"] = ["price"]
    assert route_from_objection(qualified_state) == "conversion"


def test_route_from_objection_two_objections_escalates(qualified_state):
    qualified_state["objections_raised"] = ["price", "delivery"]
    assert route_from_objection(qualified_state) == "escalation"


def test_route_from_objection_explicit_escalation(qualified_state):
    qualified_state["escalated"] = True
    assert route_from_objection(qualified_state) == "escalation"
