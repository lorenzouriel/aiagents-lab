# Routing — LangChain
Uses `RunnableBranch` to classify customer requests with an LLM and route them to the appropriate specialist chain (booking, info, or clarification).

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
python 02_routing/langchain/main.py
```

## How it works
```
Request → [Router LLM] → booking | info | unclear → [Specialist Chain] → Response
```

A `router_chain` classifies the intent into one of three categories. A `RunnableBranch` dispatches the request to the matching handler chain based on that classification.
