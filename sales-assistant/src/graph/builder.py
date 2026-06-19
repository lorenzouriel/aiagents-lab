from functools import partial

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, StateGraph
from psycopg_pool import AsyncConnectionPool
from sqlalchemy.ext.asyncio import AsyncSession

from src.graph.nodes.classifier import classifier_node, route_from_classifier
from src.graph.nodes.conversion import conversion_node, route_from_conversion
from src.graph.nodes.discovery import discovery_node, route_from_discovery
from src.graph.nodes.escalation import escalation_node
from src.graph.nodes.objection import objection_node, route_from_objection
from src.graph.nodes.recommendation import recommendation_node, route_from_recommendation
from src.graph.nodes.support import route_from_support, support_node
from src.graph.state import ConversationState

_compiled_graph = None
_pool: AsyncConnectionPool | None = None


async def init_graph(db_url: str) -> None:
    global _compiled_graph, _pool

    raw_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    _pool = AsyncConnectionPool(
        conninfo=raw_url,
        max_size=20,
        kwargs={"autocommit": True, "prepare_threshold": 0},
        open=False,
    )
    await _pool.open()

    checkpointer = AsyncPostgresSaver(_pool)
    await checkpointer.setup()

    _compiled_graph = _build(checkpointer)


async def close_graph() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()


def get_compiled_graph():
    if _compiled_graph is None:
        raise RuntimeError("Graph not initialised — call init_graph() first")
    return _compiled_graph


def _build(checkpointer: AsyncPostgresSaver):
    graph = StateGraph(ConversationState)

    # Nodes that need db session are wrapped with a factory at call time
    graph.add_node("classifier", classifier_node)
    graph.add_node("discovery", discovery_node)
    graph.add_node("recommendation", _db_node(recommendation_node))
    graph.add_node("objection_handler", _db_node(objection_node))
    graph.add_node("conversion", conversion_node)
    graph.add_node("post_sale_support", _db_node(support_node))
    graph.add_node("escalation", escalation_node)

    graph.set_entry_point("classifier")

    graph.add_conditional_edges("classifier", route_from_classifier, {
        "discovery": "discovery",
        "recommendation": "recommendation",
        "post_sale_support": "post_sale_support",
        "escalation": "escalation",
    })
    graph.add_conditional_edges("discovery", route_from_discovery, {
        "discovery": "discovery",
        "recommendation": "recommendation",
        "escalation": "escalation",
    })
    graph.add_conditional_edges("recommendation", route_from_recommendation, {
        "conversion": "conversion",
        "objection_handler": "objection_handler",
        "escalation": "escalation",
    })
    graph.add_conditional_edges("objection_handler", route_from_objection, {
        "conversion": "conversion",
        "escalation": "escalation",
    })
    graph.add_conditional_edges("conversion", route_from_conversion, {
        "__end__": END,
        "escalation": "escalation",
    })
    graph.add_conditional_edges("post_sale_support", route_from_support, {
        "__end__": END,
        "escalation": "escalation",
    })
    graph.add_edge("escalation", END)

    return graph.compile(checkpointer=checkpointer)


def _db_node(node_fn):
    """Wrap a node function that requires a DB session."""
    from src.db.postgres import AsyncSessionFactory

    async def wrapper(state: ConversationState) -> dict:
        async with AsyncSessionFactory() as db:
            return await node_fn(state, db)

    wrapper.__name__ = node_fn.__name__
    return wrapper
