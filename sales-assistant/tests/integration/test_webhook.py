import pytest
import respx
import httpx
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


TEXT_WEBHOOK_PAYLOAD = {
    "event": "messages.upsert",
    "instance": "sales-agent",
    "data": {
        "key": {
            "remoteJid": "5511999990001@s.whatsapp.net",
            "fromMe": False,
            "id": "TEST-MSG-001",
        },
        "messageType": "conversation",
        "message": {"conversation": "Oi, quero saber mais sobre vocês"},
    },
}

IGNORED_PAYLOAD = {
    "event": "messages.upsert",
    "instance": "sales-agent",
    "data": {
        "key": {"remoteJid": "5511999990001@s.whatsapp.net", "fromMe": True, "id": "MY-MSG"},
        "messageType": "conversation",
        "message": {"conversation": "Sent by bot"},
    },
}


@pytest.mark.asyncio
async def test_webhook_ignores_own_messages():
    with patch("src.graph.builder.init_graph"), \
         patch("src.graph.builder.close_graph"), \
         patch("src.db.redis.close_redis"):
        from src.main import app
        client = TestClient(app)
        resp = client.post("/webhook/evolution", json=IGNORED_PAYLOAD)
        assert resp.status_code == 200
        assert resp.json()["status"] == "ignored"


@pytest.mark.asyncio
async def test_webhook_accepts_text_message_and_returns_received():
    with patch("src.graph.builder.init_graph"), \
         patch("src.graph.builder.close_graph"), \
         patch("src.db.redis.close_redis"):
        from src.main import app
        client = TestClient(app)
        resp = client.post("/webhook/evolution", json=TEXT_WEBHOOK_PAYLOAD)
        assert resp.status_code == 200
        assert resp.json()["status"] == "received"


@pytest.mark.asyncio
async def test_webhook_ignores_unknown_event_type():
    payload = {**TEXT_WEBHOOK_PAYLOAD, "event": "connection.update"}
    with patch("src.graph.builder.init_graph"), \
         patch("src.graph.builder.close_graph"), \
         patch("src.db.redis.close_redis"):
        from src.main import app
        client = TestClient(app)
        resp = client.post("/webhook/evolution", json=payload)
        assert resp.json()["status"] == "ignored"
