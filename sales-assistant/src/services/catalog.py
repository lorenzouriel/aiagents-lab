import json

import structlog
from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models.product import Product

log = structlog.get_logger()
_openai = AsyncOpenAI(api_key=settings.openai_api_key)


async def get_embedding(text: str) -> list[float]:
    response = await _openai.embeddings.create(
        model=settings.openai_embedding_model,
        input=text,
    )
    return response.data[0].embedding


async def search_products(
    query: str,
    db: AsyncSession,
    top_k: int = 3,
    in_stock_only: bool = True,
) -> list[Product]:
    embedding = await get_embedding(query)
    stmt = (
        select(Product)
        .order_by(Product.embedding.cosine_distance(embedding))
        .limit(top_k)
    )
    if in_stock_only:
        stmt = stmt.where(Product.in_stock.is_(True))
    result = await db.execute(stmt)
    products = list(result.scalars().all())
    log.info("catalog_search", query_len=len(query), results=len(products))
    return products


async def get_cross_sell(
    primary_product_id: str,
    db: AsyncSession,
    top_k: int = 1,
) -> list[Product]:
    primary = await db.get(Product, primary_product_id)
    if not primary or primary.embedding is None:
        return []
    stmt = (
        select(Product)
        .where(Product.category == primary.category)
        .where(Product.product_id != primary_product_id)
        .where(Product.in_stock.is_(True))
        .order_by(Product.embedding.cosine_distance(primary.embedding))
        .limit(top_k)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


def products_to_json(products: list[Product]) -> str:
    return json.dumps(
        [
            {
                "id": p.product_id,
                "name": p.name,
                "price": float(p.price),
                "description": p.description or "",
                "purchase_url": p.purchase_url or "",
            }
            for p in products
        ],
        ensure_ascii=False,
    )
