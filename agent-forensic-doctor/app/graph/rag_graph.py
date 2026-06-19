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
from app.graph.prompt import SYSTEM_PROMPT_FORENSE


langfuse_handler = CallbackHandler()


# =========================
# Graph State Definitions
# =========================
class RAGState(TypedDict):
    question: str
    docs: List[Document]
    answer: Generator[str, None, None]
    generated_query: str
    generated_filter: str
    messages: Annotated[list, add_messages]


# =========================
# Helper Functions
# =========================
def _format_filter_for_display(filter_obj: Any) -> str:
    """Format structured filter into a human-readable string."""
    if not filter_obj:
        return "Nenhum filtro aplicado."

    raw_str = str(filter_obj)
    raw_str = re.sub(r"Operation\(operator=<Operator\..*?>,\s*arguments=", "", raw_str)

    raw_str = re.sub(
        r"Comparator\(attribute='(.*?)',\s*operator=<Comparator\..*?>,\s*value='(.*?)'\)",
        r"\1 = '\2'",
        raw_str,
    )

    raw_str = raw_str.replace("[", "").replace("]", "").replace("),", " E ")
    raw_str = raw_str.strip("()")

    return raw_str if raw_str else "Nenhum filtro aplicado."


def _format_docs(docs: List[Document]) -> str:
    """Format forensic documents for LLM context."""
    parts = []

    for d in docs:
        md = d.metadata or {}

        head = (
            f"[Arquivo: {md.get('pdf_name', '?')} | "
            f"Caso: {md.get('case_id', '?')} | "
            f"Tipo: {md.get('document_type', '?')} | "
            f"Seção: {md.get('section', '?')}]"
            f"\nData do Documento: {md.get('document_date', 'não informado')}"
            f"\nConfiança: {md.get('confidence_level', 'não informado')}"
        )

        parts.append(f"{head}\n\n{d.page_content}")

    return "\n\n---\n\n".join(parts)


# =========================
# Graph Nodes
# =========================
def retrieve(
    state: RAGState,
    config: RunnableConfig,
    collection_name: str = "forensic_cases",
    k: int = 10,
) -> Dict[str, Any]:
    """Executes SelfQueryRetriever and extracts generated query + filters."""
    print("[INFO] - Executing retriever node...")

    cfg = SelfQueryConfig(collection_name=collection_name, k=k)
    retriever = build_self_query_retriever(cfg)

    structured_query: StructuredQuery = retriever.query_constructor.invoke(
        {"query": state["question"]}, config=config
    )

    docs = retriever.invoke(state["question"], config=config)

    print(f"[SUCCESS] - Retriever finished. {len(docs)} documents find.")

    return {
        "docs": docs,
        "generated_query": structured_query.query,
        "generated_filter": _format_filter_for_display(structured_query.filter),
    }


def generate_stream(state: RAGState, config: RunnableConfig) -> Dict[str, Any]:
    """Generates the final forensic answer in streaming mode."""
    print("[INFO] - Executing generation node...")

    QA_PROMPT = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_FORENSE),
            (
                "human",
                "Pergunta: {question}\n\n"
                "Contexto (trechos periciais):\n{context}\n\n"
                "Responda **exclusivamente com base nos documentos fornecidos**.",
            ),
        ]
    )

    embedder = EmbeddingSelfQuery()
    llm = embedder.llm

    context = _format_docs(state.get("docs", []))

    chain = QA_PROMPT | llm | StrOutputParser()

    answer_stream = chain.stream(
        {
            "question": state["question"],
            "context": context,
        },
        config=config,
    )

    return {"answer": answer_stream}

# =========================
# Graph Builder
# =========================
def build_streaming_graph(
    collection_name: str = "forensic_cases",
    k: int = 5,
):
    """Compiles the LangGraph pipeline for forensic streaming RAG."""
    graph = StateGraph(RAGState)

    graph.add_node(
        "retrieve",
        lambda s, config: retrieve(
            s,
            config=config,
            collection_name=collection_name,
            k=k,
        ),
    )

    graph.add_node("generate", generate_stream)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


# =========================
# Compiled Graph Instance
# =========================
COMPILED_GRAPH = build_streaming_graph()


# =========================
# Main Function (Frontend)
# =========================
def run_streaming_rag(question: str) -> Generator[Dict[str, Any], None, None]:
    """
    Runs the forensic RAG streaming graph and yields events for the frontend.
    """

    run_config = RunnableConfig(
        callbacks=[langfuse_handler],
        run_name="Forensic-Chat",
        tags=["cases", "forensic", "rag"],
        metadata={
            "collection": "forensic_cases",
            "k": 5,
            "user": "Lorenzo Uriel",
        },
    )

    initial_state: RAGState = {
        "question": question,
        "messages": [],
    }

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
            for token in answer_stream:
                yield {"type": "token", "data": token}

        if END in event:
            final_state = event[END]

    # =========================
    # Final Source Listing
    # =========================
    docs = final_state.get("docs", [])

    sources = [
        {
            "case_id": d.metadata.get("case_id"),
            "document_type": d.metadata.get("document_type"),
            "pdf_name": d.metadata.get("pdf_name"),
            "document_date": d.metadata.get("document_date"),
            "section": d.metadata.get("section"),
            "confidence_level": d.metadata.get("confidence_level"),
        }
        for d in docs
    ]

    yield {"type": "sources", "data": sources}