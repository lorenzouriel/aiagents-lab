import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class LeadStage(str, Enum):
    NEW = "new"
    QUALIFYING = "qualifying"
    RECOMMENDING = "recommending"
    OBJECTING = "objecting"
    CONVERTING = "converting"
    SUPPORT = "support"
    ESCALATED = "escalated"
    COLD = "cold"


class LeadTemperature(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class Lead(Base):
    __tablename__ = "leads"

    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(100))
    lead_stage: Mapped[str] = mapped_column(String(30), nullable=False, default=LeadStage.NEW)
    lead_temperature: Mapped[str] = mapped_column(
        String(10), nullable=False, default=LeadTemperature.COLD
    )
    budget_signal: Mapped[str | None] = mapped_column(String(100))
    product_interest: Mapped[str | None] = mapped_column(Text)
    urgency: Mapped[str | None] = mapped_column(String(10))
    last_message_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    escalated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    follow_up_scheduled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
