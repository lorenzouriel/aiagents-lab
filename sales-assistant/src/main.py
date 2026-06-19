from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from src.api.health import router as health_router
from src.api.internal import router as internal_router
from src.api.webhook import router as webhook_router
from src.config import settings
from src.db.redis import close_redis
from src.graph.builder import close_graph, init_graph

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("startup_begin")
    await init_graph(settings.database_url)
    log.info("graph_ready")
    yield
    await close_graph()
    await close_redis()
    log.info("shutdown_complete")


app = FastAPI(title="WPP AI Sales Agent", version="0.1.0", lifespan=lifespan)
app.include_router(health_router)
app.include_router(webhook_router)
app.include_router(internal_router)
