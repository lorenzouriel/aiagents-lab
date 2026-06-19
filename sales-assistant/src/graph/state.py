from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class LeadProfile(TypedDict, total=False):
    lead_id: str
    phone_number: str
    name: str
    budget_signal: str
    product_interest: str
    urgency: str        # high | medium | low
    temperature: str    # hot | warm | cold


class ConversationState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    lead_id: str
    phone_number: str
    current_stage: str
    lead_profile: LeadProfile
    products_recommended: list[str]
    objections_raised: list[str]
    escalated: bool
    follow_up_scheduled: bool
    turn_count: int
