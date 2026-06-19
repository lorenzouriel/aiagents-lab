"""Internal endpoints called by Kestra workflows."""
import structlog
from fastapi import APIRouter, Request
from langchain_core.messages import HumanMessage
from sqlalchemy import select

from src.db.postgres import AsyncSessionFactory
from src.graph.builder import get_compiled_graph
from src.models.lead import Lead
from src.services.catalog import get_embedding
from src.services.memory import save_conversation_summary
from src.services.nuvemshop import fetch_all_products

log = structlog.get_logger()
router = APIRouter(prefix="/internal")


@router.post("/sync-catalog")
async def sync_catalog():
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    from src.models.product import Product

    products = await fetch_all_products()
    async with AsyncSessionFactory() as db:
        for p in products:
            text = f"{p.name}. {p.description or ''}".strip()
            embedding = await get_embedding(text)
            stmt = (
                pg_insert(Product)
                .values(
                    product_id=p.product_id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    category=p.category,
                    in_stock=p.in_stock,
                    purchase_url=p.purchase_url,
                    embedding=embedding,
                )
                .on_conflict_do_update(
                    index_elements=["product_id"],
                    set_={
                        "name": p.name,
                        "description": p.description,
                        "price": p.price,
                        "in_stock": p.in_stock,
                        "embedding": embedding,
                    },
                )
            )
            await db.execute(stmt)
        await db.commit()
    log.info("catalog_synced", count=len(products))
    return {"synced": len(products)}


@router.post("/summarize")
async def summarize_conversation(request: Request):
    body = await request.json()
    phone = body.get("phone_number")
    lead_id = body.get("lead_id")
    if not phone or not lead_id:
        return {"status": "missing_params"}

    graph = get_compiled_graph()
    config = {"configurable": {"thread_id": phone}}
    state = await graph.aget_state(config)
    if not state or not state.values:
        return {"status": "no_state"}

    values = state.values
    messages = values.get("messages", [])
    conversation_text = "\n".join(
        f"{'Cliente' if m.type == 'human' else 'Lia'}: {m.content}"
        for m in messages[-20:]
    )

    from openai import AsyncOpenAI
    from src.config import settings
    openai = AsyncOpenAI(api_key=settings.openai_api_key)
    resp = await openai.chat.completions.create(
        model=settings.openai_model_default,
        messages=[
            {
                "role": "system",
                "content": (
                    "Resuma esta conversa de vendas em 3 linhas: "
                    "1) interesse do cliente, 2) produtos discutidos, 3) resultado (converteu/frio/escalado). "
                    "Responda em português."
                ),
            },
            {"role": "user", "content": conversation_text},
        ],
    )
    summary_text = resp.choices[0].message.content

    profile = values.get("lead_profile", {})
    import uuid
    async with AsyncSessionFactory() as db:
        await save_conversation_summary(
            lead_id=uuid.UUID(lead_id),
            db=db,
            intent=profile.get("product_interest"),
            products_discussed=values.get("products_recommended", []),
            outcome=values.get("current_stage"),
            temperature=profile.get("temperature"),
            summary_text=summary_text,
        )

    return {"status": "summarized"}
