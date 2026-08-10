"""
Knowledge Retrieval (RAG) with LangChain
==========================================
Demonstrates a full RAG pipeline: document loading, chunking,
embedding, vector storage, retrieval, and augmented generation.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# --- Simulated Document Store (in production: FAISS, Pinecone, etc.) ---

DOCUMENTS = [
    "Our return policy allows returns within 30 days with receipt. Items must be in original condition.",
    "Free shipping on orders over $50. Standard shipping takes 5-7 business days. Express: 2-3 days for $12.",
    "Loyalty members earn 2 points per dollar spent. 500 points = $10 reward. Sign up is free.",
    "We accept Visa, Mastercard, American Express, PayPal, and Apple Pay. No checks or cash on delivery.",
]

def simple_retriever(query: str, top_k: int = 2) -> list:
    """Simple keyword-based retriever (in production: use embeddings + vector DB)."""
    scored = []
    for doc in DOCUMENTS:
        score = sum(1 for w in query.lower().split() if w in doc.lower())
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:top_k] if score > 0]


# --- RAG Chain ---

rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Answer the question based ONLY on the provided context. "
     "If the context doesn't contain the answer, say so."),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])
rag_chain = rag_prompt | llm | parser


def rag_query(question: str) -> str:
    docs = simple_retriever(question)
    context = "\n".join(f"[{i+1}] {doc}" for i, doc in enumerate(docs))
    print(f"  Retrieved {len(docs)} documents")
    return rag_chain.invoke({"context": context, "question": question})


if __name__ == "__main__":
    questions = [
        "What is your return policy?",
        "Do you offer free shipping?",
        "How does the loyalty program work?",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {rag_query(q)}")
