import json
from dataclasses import dataclass
from pathlib import Path

import httpx
import structlog

from src.config import settings

log = structlog.get_logger()

_BASE = f"https://api.tiendanube.com/v1/{settings.nuvemshop_store_id}"
_HEADERS = {
    "Authentication": f"1 {settings.nuvemshop_access_token}",
    "User-Agent": "WPP-AI-Sales-Agent/1.0 (lorenzouriel394@gmail.com)",
    "Content-Type": "application/json",
}

_MOCK_CATALOG_PATH = Path(__file__).parent.parent.parent / "mock" / "catalog.json"


@dataclass
class NuvemshopProduct:
    product_id: str
    name: str
    description: str
    price: float
    category: str
    in_stock: bool
    purchase_url: str


async def fetch_all_products() -> list[NuvemshopProduct]:
    if settings.nuvemshop_mock:
        return _load_mock_catalog()
    return await _fetch_from_api()


async def fetch_order(order_number: str) -> dict | None:
    if settings.nuvemshop_mock:
        return _mock_order(order_number)
    return await _fetch_order_from_api(order_number)


# ── Mock implementations ───────────────────────────────────────────────────────

def _load_mock_catalog() -> list[NuvemshopProduct]:
    raw = json.loads(_MOCK_CATALOG_PATH.read_text(encoding="utf-8"))
    products = [
        NuvemshopProduct(
            product_id=str(p["id"]),
            name=p["name"],
            description=p.get("description", ""),
            price=float(p["price"]),
            category=p.get("category", ""),
            in_stock=p.get("in_stock", True),
            purchase_url=p.get("purchase_url", ""),
        )
        for p in raw
    ]
    log.info("mock_catalog_loaded", count=len(products))
    return products


def _mock_order(order_number: str) -> dict:
    return {
        "number": order_number,
        "status": "paid",
        "shipping_status": "shipped",
        "shipping_tracking_number": f"BR{order_number}123BR",
        "shipping_carrier_name": "Correios PAC",
        "estimated_delivery_date": "2026-05-24",
        "products": [{"name": "Hidratante Facial Levíssimo", "quantity": 1}],
    }


# ── Real API implementations ───────────────────────────────────────────────────

async def _fetch_from_api() -> list[NuvemshopProduct]:
    products: list[NuvemshopProduct] = []
    page = 1
    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            resp = await client.get(
                f"{_BASE}/products",
                headers=_HEADERS,
                params={"per_page": 200, "page": page},
            )
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            for p in batch:
                products.append(_parse_product(p))
            if len(batch) < 200:
                break
            page += 1
    log.info("nuvemshop_products_fetched", count=len(products))
    return products


async def _fetch_order_from_api(order_number: str) -> dict | None:
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{_BASE}/orders",
            headers=_HEADERS,
            params={"q": order_number},
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        orders = resp.json()
        return orders[0] if orders else None


def _parse_product(raw: dict) -> NuvemshopProduct:
    name = raw.get("name", {})
    if isinstance(name, dict):
        name = name.get("pt", next(iter(name.values()), ""))

    desc = raw.get("description", {})
    if isinstance(desc, dict):
        desc = desc.get("pt", next(iter(desc.values()), ""))

    variants = raw.get("variants", [{}])
    price = float(variants[0].get("price", 0)) if variants else 0.0
    stock = sum(v.get("stock", 0) or 0 for v in variants)

    categories = raw.get("categories", [])
    category = categories[0].get("name", {}) if categories else {}
    if isinstance(category, dict):
        category = category.get("pt", "")

    return NuvemshopProduct(
        product_id=str(raw["id"]),
        name=name,
        description=desc or "",
        price=price,
        category=category,
        in_stock=stock > 0,
        purchase_url=raw.get("permalink", ""),
    )
