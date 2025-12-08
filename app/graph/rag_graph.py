from typing import Annotated, List, Dict, Any, Generator, TypedDict
import re

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.structured_query import StructuredQuery
from langfuse.langchain import CallbackHandler
from langchain_core.runnables import RunnableConfig

from app.ingest.embed_qdrant import EmbeddingSelfQuery
from app.retrieval.retriever import build_self_query_retriever, SelfQueryConfig
from app.graph.prompt import SYSTEM_PROMPT_JURIDICO

langfuse_handler = CallbackHandler()

# Graph State Definitions
class RAGState(TypedDict):
    question: str
    docs: List[Document]
    answer: Generator[str, None, None]
    generated_query: str
    generated_filter: str
    messages: Annotated[list, add_messages]

# --- Function ---
def _format_filter_for_display(filter_obj: Any) -> str:
    """Format the filter object into a human-readable string."""
    if not filter_obj:
        return "Non-applied filter."
    raw_str = str(filter_obj)
    raw_str = re.sub(r"Operation\(operator=<Operator\..*?>,\s*arguments=", "", raw_str)
    raw_str = re.sub(
        r"Comparator\(attribute='(.*?)',\s*operator=<Comparator\..*?>,\s*value='(.*?)'\)",
        r"\1 = '\2'",
        raw_str,
    )
    raw_str = raw_str.replace("[", "").replace("]", "").replace("),", " E ")
    raw_str = raw_str.strip("()")
    return raw_str if raw_str else "Non-applied filter."

def _format_docs(docs: List[Document]) -> str:
    parts = []
    for d in docs:
        md = d.metadata or {}
        head = (
            f"[{md.get('pdf_name', '?')} | Súmula {md.get('num_sumula', '?')} | {md.get('chunk_type', 'chunk')}]"
            f"\nstatus_atual: {md.get('status_atual', 'não informado')}"
            f"\ndata_status: {md.get('data_status', 'não informado')}"
        )
        parts.append(f"{head}\n\n{d.page_content}")
    return "\n\n---\n\n".join(parts)


# --- Graph Nodes ---
def retrieve(
    state: RAGState,
    config: RunnableConfig,
    collection_name: str = "cases",
    k: int = 10,
) -> Dict[str, Any]:
    """Node that executes SelfQueryRetriever and extract details of the generated query."""
    print("Executing recovery node..")
    cfg = SelfQueryConfig(collection_name=collection_name, k=k)
    retriever = build_self_query_retriever(cfg)

    structured_query: StructuredQuery = retriever.query_constructor.invoke(
        {"query": state["question"]}, config=config
    )
    docs = retriever.invoke(state["question"], config=config)

    print(f"Query finished. Find {len(docs)} documents.")
    return {
        "docs": docs,
        "generated_query": structured_query.query,
        "generated_filter": _format_filter_for_display(structured_query.filter),
    }


def generate_stream(state: RAGState, config: RunnableConfig) -> Dict[str, Any]:
    """Node that generates final answers in a stream format."""
    print("Executin generation node...")
    QA_PROMPT = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_JURIDICO),
            (
                "human",
                "Pergunta: {question}\n\nContexto (trechos):\n{context}\n\nResponda de forma direta. Ao final, liste fontes no formato: (Status: metadata.status_atual, Documento: metadata.num_sumula, Data da Publicação:  metadata.data_status).",
            ),
        ]
    )

    embedder = EmbeddingSelfQuery()
    llm = embedder.llm
    context = _format_docs(state.get("docs", []))
    chain = QA_PROMPT | llm | StrOutputParser()

    answer_stream = chain.stream(
        {"question": state["question"], "context": context},
        config=config,
    )
    return {"answer": answer_stream}

# --- Graph Builder ---
def build_streaming_graph(collection_name: str = "cases", k: int = 5):
    """Compile language graph for streaming RAG."""
    graph = StateGraph(RAGState)
    graph.add_node(
        "retrieve",
        lambda s, config: retrieve(
            s, config=config, collection_name=collection_name, k=k
        ),
    )
    graph.add_node("generate", generate_stream)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()

# Compiled Graph Instance to be used
COMPILED_GRAPH = build_streaming_graph()

# --- Main function (to be used by the frontend) ---
def run_streaming_rag(question: str) -> Generator[Dict[str, Any], None, None]:
    """
    Function that runs the RAG streaming graph and yields events for the frontend.
    """

    run_config = RunnableConfig(
        callbacks=[langfuse_handler],
        run_name="Chat",
        tags=["live-demo", "sumulas"],
        metadata={"collection": "cases", "k": 5, "user": "Caio"},
    )

    initial_state: RAGState = {"question": question, "messages": []}
    final_state = {}

    # Execute graph and stream events
    for event in COMPILED_GRAPH.stream(initial_state, config=run_config):
        if "retrieve" in event:
            output = event["retrieve"]
            yield {
                "type": "details",
                "data": {
                    "query": output["generated_query"],
                    "filter": output["generated_filter"],
                },
            }

        if "generate" in event:
            answer_stream = event["generate"]["answer"]
            # Transmit each token as it is generated
            for token in answer_stream:
                yield {"type": "token", "data": token}

        if END in event:
            final_state = event[END]

    # Format and yield sources information
    docs = final_state.get("docs", [])
    sources = [
        {
            "pdf_name": d.metadata.get("pdf_name"),
            "data_status": d.metadata.get("data_status"),
            "data_status_ano": d.metadata.get("data_status_ano"),
            "status_atual": d.metadata.get("status_atual"),
            "num_sumula": d.metadata.get("num_sumula"),
            "chunk_type": d.metadata.get("chunk_type"),
        }
        for d in docs
    ]
    yield {"type": "sources", "data": sources}