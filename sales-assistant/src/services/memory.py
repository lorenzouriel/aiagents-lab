import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.conversation_summary import ConversationSummary
from src.models.lead import Lead

log = structlog.get_logger()


async def get_or_create_lead(phone_number: str, db: AsyncSession) -> Lead:
    result = await db.execute(select(Lead).where(Lead.phone_number == phone_number))
    lead = result.scalar_one_or_none()
    if lead is None:
        lead = Lead(phone_number=phone_number)
        db.add(lead)
        await db.commit()
        await db.refresh(lead)
        log.info("lead_created", lead_id=str(lead.lead_id))
    return lead


async def update_lead(phone_number: str, db: AsyncSession, **fields) -> None:
    fields["last_message_at"] = datetime.now(tz=timezone.utc)
    await db.execute(
        update(Lead).where(Lead.phone_number == phone_number).values(**fields)
    )
    await db.commit()


async def save_conversation_summary(
    lead_id: uuid.UUID,
    db: AsyncSession,
    intent: str | None = None,
    products_discussed: list[str] | None = None,
    outcome: str | None = None,
    temperature: str | None = None,
    summary_text: str | None = None,
) -> None:
    summary = ConversationSummary(
        lead_id=lead_id,
        intent=intent,
        products_discussed=products_discussed or [],
        outcome=outcome,
        temperature=temperature,
        summary_text=summary_text,
    )
    db.add(summary)
    await db.commit()
    log.info("summary_saved", lead_id=str(lead_id), outcome=outcome)
