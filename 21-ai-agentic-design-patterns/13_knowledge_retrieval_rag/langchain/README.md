# Knowledge Retrieval (RAG) — LangChain
A full Retrieval-Augmented Generation pipeline: a keyword-based retriever fetches relevant documents from a simulated store, and the LLM generates an answer grounded in that context.

## Setup
```bash
# From the project root
source .venv/Scripts/activate
pip install -r requirements.txt
# PowerShell
$env:OPENAI_API_KEY="sk-..."

# bash/zsh
export OPENAI_API_KEY="sk-..."
```

## Run
```bash
python 13_knowledge_retrieval_rag/langchain/main.py
```

## How it works
```
Question → [Retriever] → top-k documents → [RAG Chain] → Grounded Answer
```

`simple_retriever` scores documents by keyword overlap and returns the top `k` matches. The RAG prompt instructs the LLM to answer **only** from the provided context, preventing hallucination. In production, replace `simple_retriever` with FAISS or Pinecone.
