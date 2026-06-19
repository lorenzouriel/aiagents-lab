# WPP AI Sales Agent

> A WhatsApp AI sales assistant powered by LangGraph, designed for Brazilian e-commerce stores on Nuvemshop. Qualifies leads, recommends products, handles objections, and schedules follow-ups — all in Portuguese, 24/7.

## Overview

The WPP AI Sales Agent connects to your WhatsApp Business number via Evolution API and runs a stateful 7-node conversation graph using LangGraph. Each conversation thread is persisted in PostgreSQL, so the agent remembers context across sessions. Products are stored as vector embeddings (pgvector) for semantic search, enabling relevant recommendations even for vague queries like "something for oily skin."

The agent persona is **Lia** — a warm, knowledgeable Brazilian beauty consultant. All prompts are in Brazilian Portuguese.

## Features

- **Lead qualification** — discovers skin type, budget, and urgency through guided conversation
- **Semantic product recommendations** — pgvector cosine similarity search across your Nuvemshop catalog
- **Cross-sell** — suggests complementary products from the same category
- **Objection handling** — detects price/delivery/doubt objections; surfaces alternatives for price pushback
- **Lead temperature scoring** — tags each lead as hot / warm / cold based on engagement signals
- **Follow-up engine** — Kestra schedules 24h / 72h / 7-day follow-ups automatically
- **Voice note transcription** — OpenAI Whisper transcribes audio messages before processing
- **Human escalation** — sends WhatsApp alert to the store owner when the agent can't resolve
- **Order status** — looks up Nuvemshop orders by number and reports shipping status
- **Conversation summaries** — periodically summarizes inactive conversations to Postgres
- **Mock mode** — develop and test locally without real Nuvemshop credentials

## Architecture

```
WhatsApp ──► Evolution API ──► POST /webhook/evolution
                                        │
                                        ▼
                              FastAPI (BackgroundTask)
                                        │
                              Redis idempotency check
                                        │
                                        ▼
                             LangGraph StateGraph
                          ┌─────────────────────────┐
                          │  classifier              │
                          │      │                   │
                          │  discovery  ◄────────┐   │
                          │      │               │   │
                          │  recommendation      │   │
                          │      │               │   │
                          │  objection_handler ──┘   │
                          │      │                   │
                          │  conversion              │
                          │      │                   │
                          │  support                 │
                          │      │                   │
                          │  escalation              │
                          └─────────────────────────┘
                                        │
                              AsyncPostgresSaver
                             (thread_id = phone_number)
                                        │
                              ┌─────────┴──────────┐
                           Postgres            Kestra
                        (leads, products,   (follow-ups,
                         pgvector, summaries) catalog sync)
```

**Stack:**
| Layer | Technology |
|-------|-----------|
| WhatsApp gateway | Evolution API v2.1.1 (self-hosted) |
| API server | FastAPI + uvicorn |
| AI orchestration | LangGraph 0.3+ StateGraph |
| LLM | gpt-4o-mini (speed) / gpt-4o (quality nodes) |
| Embeddings | text-embedding-3-small (1536 dims) |
| Voice transcription | OpenAI Whisper (whisper-1, pt-BR) |
| Vector search | PostgreSQL 16 + pgvector (ivfflat index) |
| Conversation memory | AsyncPostgresSaver (psycopg3) |
| Follow-up scheduling | Kestra workflow orchestration |
| Cache / idempotency | Redis 7 |
| E-commerce catalog | Nuvemshop (Tiendanube) API v1 |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- A secure Evolution API key that you generate
- Nuvemshop store ID and access token (or use mock mode)

### 1. Clone and configure

```bash
git clone <repo-url> wpp-ai-sales-agent
cd wpp-ai-sales-agent

cp docker/.env.example .env
# Edit .env with your credentials (see Configuration section below)
```

Generate an Evolution API key with PowerShell:

```powershell
[guid]::NewGuid().ToString("N")
```

For local development, use these important `.env` values:

```env
OPENAI_API_KEY=your-real-openai-key
EVOLUTION_API_KEY=your-generated-secret
EVOLUTION_API_URL=http://evolution-api:8080
EVOLUTION_INSTANCE_NAME=sales-agent
NUVEMSHOP_MOCK=true
DATABASE_URL=postgresql+asyncpg://salesagent:changeme@postgres:5432/sales_agent
REDIS_URL=redis://redis:6379
KESTRA_URL=http://kestra:8080
```

### 2. Start the stack

Run from the **project root**, passing the env file explicitly:

```bash
docker compose -f docker/docker-compose.yml --env-file .env up -d
```

Services:
- **App** — `http://localhost:8000`
- **Evolution API** — `http://localhost:8080`
- **Kestra** — `http://localhost:8088`
- **Postgres** — `localhost:5432`
- **Redis** — `localhost:6379`

Postgres is exposed as `localhost:5433` for host tools. Containers connect to `postgres:5432`.

### 3. Embed the catalog (one-time)

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec app python scripts/embed_catalog.py
```

This fetches products from Nuvemshop (or mock), generates embeddings, and populates the `products` table.

### 4. Connect WhatsApp

Evolution API `v2.3.7` is included in Docker Compose. Numeric pairing is the recommended connection
method. Create the instance, configure its webhook, and request a pairing code with PowerShell:

```powershell
$key = (Get-Content .env | Where-Object { $_ -match '^EVOLUTION_API_KEY=' }).Split('=', 2)[1]
$headers = @{ apikey = $key; "Content-Type" = "application/json" }

$body = @{
    instanceName = "sales-agent"
    integration = "WHATSAPP-BAILEYS"
    qrcode = $true
    number = "5511999999999"
    groupsIgnore = $true
    webhook = @{
        url = "http://app:8000/webhook/evolution"
        byEvents = $false
        base64 = $false
        events = @("MESSAGES_UPSERT")
    }
} | ConvertTo-Json -Depth 6

$result = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8080/instance/create" `
    -Headers $headers `
    -Body $body

$result.qrcode.pairingCode
```

Replace the example number with the store WhatsApp number in E.164 format. In WhatsApp, open
**Settings > Linked devices > Link a device > Link with phone number instead**, then enter the
pairing code immediately.

If the `sales-agent` instance already exists, request a fresh pairing code:

```powershell
Invoke-RestMethod `
    -Uri "http://localhost:8080/instance/connect/sales-agent?number=5511999999999" `
    -Headers @{ apikey = $key }
```

Alternatively, use QR pairing:

1. Open `http://localhost:8080` in your browser
2. Go to **Instances** → **sales-agent** → **Connect**
3. Scan the QR code with the store's WhatsApp

### 5. Register or verify the webhook

The instance creation request above configures the webhook automatically. Use this endpoint if you
created the instance manually or need to replace its webhook:

```powershell
Invoke-RestMethod `
    -Uri "http://localhost:8080/webhook/find/sales-agent" `
    -Headers @{ apikey = $key }
```

### 6. Verify

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

Send a WhatsApp message to the connected number — Lia should respond within a few seconds.

### End-to-end WhatsApp test

The test message must come from a **different WhatsApp account** because messages sent by the
connected account itself are ignored. A useful first message is:

```text
Oi, estou procurando um hidratante para pele oleosa
```

Watch the complete message flow:

```bash
docker compose -f docker/docker-compose.yml --env-file .env logs -f app evolution-api
```

Verify the Evolution connection state:

```powershell
Invoke-RestMethod `
    -Uri "http://localhost:8080/instance/connectionState/sales-agent" `
    -Headers @{ apikey = $key }
```

If WhatsApp remains on **Logging in**, wait briefly and check the connection state. Evolution may be
synchronizing contacts and message sessions after the first successful link.

## Mock Mode (Local Development)

To develop without real Nuvemshop credentials, set `NUVEMSHOP_MOCK=true` in `.env`. The agent will read from `mock/catalog.json` (16 Brazilian beauty products) instead of calling the API.

```bash
NUVEMSHOP_MOCK=true
# NUVEMSHOP_STORE_ID and NUVEMSHOP_ACCESS_TOKEN are not required in mock mode
```

Order lookup in mock mode always returns a fake shipped order for any order number.

## Configuration

All settings are loaded from `.env` via Pydantic Settings.

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI API key | — |
| `EVOLUTION_API_URL` | Yes | Evolution API base URL | — |
| `EVOLUTION_API_KEY` | Yes | Evolution API authentication key | — |
| `EVOLUTION_INSTANCE_NAME` | Yes | WhatsApp instance name | — |
| `NUVEMSHOP_STORE_ID` | No* | Nuvemshop store ID | `mock` |
| `NUVEMSHOP_ACCESS_TOKEN` | No* | Nuvemshop access token | `mock` |
| `NUVEMSHOP_MOCK` | No | Use local mock catalog instead of API | `false` |
| `POSTGRES_USER` | Yes | Postgres username | — |
| `POSTGRES_PASSWORD` | Yes | Postgres password | — |
| `POSTGRES_DB` | Yes | Postgres database name | — |
| `DATABASE_URL` | Yes | Full async DB URL (`postgresql+asyncpg://...`) | — |
| `REDIS_URL` | No | Redis connection URL | `redis://redis:6379` |
| `KESTRA_URL` | No | Kestra API base URL | `http://kestra:8080` |
| `OWNER_PHONE_NUMBER` | Yes | Store owner's WhatsApp in E.164 format (e.g. `5511999999999`) | — |
| `MAX_DISCOVERY_TURNS` | No | Max turns before forcing recommendation | `3` |
| `RESPONSE_TIMEOUT_SECONDS` | No | Background task timeout | `30` |

*Required when `NUVEMSHOP_MOCK=false`

## Project Structure

```
wpp-ai-sales-agent/
├── src/
│   ├── main.py                    # FastAPI app + lifespan
│   ├── config.py                  # Pydantic Settings
│   ├── api/
│   │   ├── webhook.py             # POST /webhook/evolution, /internal/followup
│   │   ├── internal.py            # POST /internal/sync-catalog, /summarize
│   │   └── health.py              # GET /health
│   ├── graph/
│   │   ├── builder.py             # LangGraph StateGraph + AsyncPostgresSaver
│   │   ├── state.py               # ConversationState TypedDict
│   │   └── nodes/
│   │       ├── classifier.py      # Intent routing
│   │       ├── discovery.py       # Lead qualification
│   │       ├── recommendation.py  # Product recommendation + cross-sell
│   │       ├── objection.py       # Objection handling
│   │       ├── conversion.py      # Closing + follow-up trigger
│   │       ├── support.py         # Post-sale / order status
│   │       └── escalation.py      # Human handoff
│   ├── services/
│   │   ├── whatsapp.py            # Evolution API client
│   │   ├── whisper.py             # Audio transcription
│   │   ├── nuvemshop.py           # Catalog + order API (+ mock)
│   │   ├── catalog.py             # pgvector semantic search
│   │   ├── memory.py              # Lead CRUD + summaries
│   │   └── kestra.py              # Follow-up scheduling
│   ├── prompts/                   # All pt-BR system prompts (Lia persona)
│   ├── models/                    # SQLAlchemy ORM models
│   ├── db/
│   │   ├── postgres.py            # Async session factory
│   │   ├── redis.py               # Redis client
│   │   └── migrations/
│   │       └── 001_initial.sql    # Schema + pgvector + indexes
│   └── utils/
│       ├── signals.py             # Lead signal extraction (budget, urgency)
│       └── scoring.py             # Lead temperature scoring
├── kestra/
│   ├── catalog-sync.yaml          # 6h catalog sync
│   ├── follow-up-24h.yaml         # 24h warm follow-up
│   ├── follow-up-72h.yaml         # 72h re-engagement
│   ├── follow-up-7d.yaml          # 7-day cold recovery
│   └── conversation-summary.yaml  # Inactive conversation summarizer
├── mock/
│   └── catalog.json               # 16 sample Brazilian beauty products
├── scripts/
│   └── embed_catalog.py           # One-time catalog embedding script
├── tests/
│   ├── unit/                      # Classifier, discovery, recommendation, objection
│   └── integration/               # Webhook endpoint, catalog search
├── docker/
│   ├── docker-compose.yml         # 5-service stack
│   └── .env.example               # Environment variable template
├── Dockerfile
└── pyproject.toml
```

## Development

### Install dependencies

```bash
pip install poetry
poetry install
```

### Run tests

```bash
poetry run pytest
```

### Lint and type check

```bash
poetry run ruff check .
poetry run mypy .
```

### Run locally (without Docker)

Start Postgres and Redis first (e.g. via Docker), then:

```bash
cp docker/.env.example .env
# Set DATABASE_URL to point to your local postgres
# Set NUVEMSHOP_MOCK=true for local dev

poetry run uvicorn src.main:app --reload --port 8000
```

## Conversation Flow

```
Incoming message
      │
      ▼
  classifier ──► new_inquiry          ──► discovery
             ──► product_question     ──► recommendation
             ──► order_status         ──► support
             ──► complaint            ──► escalation
             ──► follow_up_response   ──► discovery

discovery ──► (budget_signal + product_interest) OR (turns >= MAX) ──► recommendation
         ──► otherwise ──► loop back

recommendation ──► objection keywords detected ──► objection_handler
              ──► no objection ──► conversion

objection_handler ──► objection count >= 2 ──► escalation
                  ──► otherwise ──► recommendation

conversion ──► frustration detected ──► escalation
          ──► otherwise ──► END (follow-up scheduled in Kestra)
```

## Kestra Workflows

Kestra runs on `http://localhost:8088`. Flows are loaded from the `kestra/` directory (mounted read-only).

| Workflow | Trigger | Action |
|----------|---------|--------|
| `catalog-sync` | Every 6 hours | Syncs Nuvemshop catalog + regenerates embeddings |
| `follow-up-24h` | Triggered by conversion node | Sends warm follow-up message |
| `follow-up-72h` | Triggered by conversion node | Sends re-engagement message |
| `follow-up-7d` | Triggered by conversion node | Sends cold recovery message |
| `conversation-summary` | Scheduled / manual | Summarizes inactive conversation to Postgres |

All workflows use HTTP callbacks to `/internal/*` endpoints — business logic stays in the Python app.

## License

MIT
