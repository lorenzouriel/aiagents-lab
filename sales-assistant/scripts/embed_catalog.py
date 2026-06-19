"""
One-time script: fetch the Nuvemshop product catalog, generate embeddings,
and upsert everything into the products table.

Usage:
    python scripts/embed_catalog.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from src.db.postgres import AsyncSessionFactory
from src.models.product import Product
from src.services.catalog import get_embedding
from src.services.nuvemshop import fetch_all_products


async def main() -> None:
    print("Fetching products from Nuvemshop...")
    nuvem_products = await fetch_all_products()
    print(f"  → {len(nuvem_products)} products fetched")

    print("Embedding and upserting into Postgres...")
    async with AsyncSessionFactory() as db:
        for idx, p in enumerate(nuvem_products, 1):
            text_for_embedding = f"{p.name}. {p.description or ''}".strip()
            embedding = await get_embedding(text_for_embedding)

            stmt = (
                insert(Product)
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
                        "category": p.category,
                        "in_stock": p.in_stock,
                        "purchase_url": p.purchase_url,
                        "embedding": embedding,
                    },
                )
            )
            await db.execute(stmt)

            if idx % 10 == 0:
                await db.commit()
                print(f"  → {idx}/{len(nuvem_products)} done")

        await db.commit()

    print(f"Done. {len(nuvem_products)} products embedded and stored.")


if __name__ == "__main__":
    asyncio.run(main())
