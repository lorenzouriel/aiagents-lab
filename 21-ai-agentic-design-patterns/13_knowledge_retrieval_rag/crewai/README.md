# Knowledge Retrieval (RAG) — CrewAI
A customer support agent searches a simulated knowledge base before answering, ensuring every response is grounded in retrieved documents rather than model hallucinations.

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
python 13_knowledge_retrieval_rag/crewai/main.py
```

## How it works
```
Question → [Support Agent] → search_knowledge(query) → retrieved docs → Grounded Answer
```

The agent's backstory instructs it to always run `search_knowledge` first. The tool performs keyword matching against `KNOWLEDGE_BASE` and returns the top-3 matching documents, which the agent uses to form its answer.
