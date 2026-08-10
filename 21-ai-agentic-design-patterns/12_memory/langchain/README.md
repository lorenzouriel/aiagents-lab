# Memory — LangChain
Demonstrates short-term conversational memory using a `MessagesPlaceholder`. The agent remembers prior turns and references them when answering follow-up questions.

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
python 12_memory/langchain/main.py
```

## How it works
```
User → chat(input) → [LLM + history] → response → append(HumanMessage + AIMessage) → next turn
```

A simple Python list acts as the in-memory store. Each call to `chat()` injects the accumulated history into the prompt via `MessagesPlaceholder`, then appends the new turn to history for future calls.
