-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Lead profiles
CREATE TABLE IF NOT EXISTS leads (
    lead_id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number     VARCHAR(20)  NOT NULL UNIQUE,
    name             VARCHAR(100),
    lead_stage       VARCHAR(30)  NOT NULL DEFAULT 'new',
    lead_temperature VARCHAR(10)  NOT NULL DEFAULT 'cold',
    budget_signal    VARCHAR(100),
    product_interest TEXT,
    urgency          VARCHAR(10),
    last_message_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    escalated        BOOLEAN      NOT NULL DEFAULT FALSE,
    follow_up_scheduled BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Product catalog with semantic embeddings
CREATE TABLE IF NOT EXISTS products (
    product_id   VARCHAR(50)    PRIMARY KEY,
    name         TEXT           NOT NULL,
    description  TEXT,
    price        DECIMAL(10, 2) NOT NULL,
    category     VARCHAR(100),
    in_stock     BOOLEAN        NOT NULL DEFAULT TRUE,
    purchase_url TEXT,
    embedding    vector(1536),
    synced_at    TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS products_embedding_idx
    ON products USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);

-- Conversation summaries (written by Kestra after inactivity)
CREATE TABLE IF NOT EXISTS conversation_summaries (
    summary_id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id           UUID        NOT NULL REFERENCES leads (lead_id),
    intent            TEXT,
    products_discussed TEXT[],
    outcome           VARCHAR(50),
    temperature       VARCHAR(10),
    summary_text      TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS summaries_lead_idx ON conversation_summaries (lead_id);
CREATE INDEX IF NOT EXISTS leads_phone_idx ON leads (phone_number);
CREATE INDEX IF NOT EXISTS leads_temperature_idx ON leads (lead_temperature);
CREATE INDEX IF NOT EXISTS leads_stage_idx ON leads (lead_stage);
