import pytest
from unittest.mock import AsyncMock, MagicMock, patch


MOCK_PRODUCTS = [
    MagicMock(product_id="1", name="Hidratante Rosto Pele Oleosa", price=89.90,
              description="Hidratante leve para pele oleosa e mista", category="Rosto",
              in_stock=True, purchase_url="https://loja.com/p/1",
              embedding=[0.1] * 1536),
    MagicMock(product_id="2", name="Sérum Vitamina C", price=119.90,
              description="Sérum antioxidante com vitamina C pura", category="Rosto",
              in_stock=True, purchase_url="https://loja.com/p/2",
              embedding=[0.2] * 1536),
    MagicMock(product_id="3", name="T��nico Facial Natural", price=59.90,
              description="Tônico com ingredientes naturais, sem álcool", category="Rosto",
              in_stock=True, purchase_url="https://loja.com/p/3",
              embedding=[0.15] * 1536),
]


@pytest.mark.asyncio
async def test_search_products_returns_results():
    from src.services.catalog import search_products

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = MOCK_PRODUCTS[:2]
    mock_db.execute.return_value = mock_result

    with patch("src.services.catalog.get_embedding", return_value=[0.1] * 1536):
        results = await search_products("hidratante pele oleosa", mock_db, top_k=2)

    assert len(results) == 2


@pytest.mark.asyncio
async def test_search_products_returns_empty_when_no_match():
    from src.services.catalog import search_products

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_result

    with patch("src.services.catalog.get_embedding", return_value=[0.1] * 1536):
        results = await search_products("produto inexistente", mock_db)

    assert results == []


@pytest.mark.asyncio
async def test_products_to_json_format():
    from src.services.catalog import products_to_json
    import json

    result = json.loads(products_to_json(MOCK_PRODUCTS[:1]))
    assert result[0]["name"] == "Hidratante Rosto Pele Oleosa"
    assert result[0]["price"] == 89.9
    assert "purchase_url" in result[0]
