import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.lead import Base


class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    summary_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    intent: Mapped[str | None] = mapped_column(Text)
    products_discussed: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    outcome: Mapped[str | None] = mapped_column(String(50))
    temperature: Mapped[str | None] = mapped_column(String(10))
    summary_text: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
