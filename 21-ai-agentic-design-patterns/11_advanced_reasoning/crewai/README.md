# Advanced Reasoning — CrewAI
A single reasoning agent uses a `search_kb` tool to look up facts about Python, Rust, and Go memory management, then synthesizes a structured, step-by-step comparison.

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
python 11_advanced_reasoning/crewai/main.py
```

## How it works
```
Question → [Reasoner Agent] → search_kb("python gc") → search_kb("rust memory") → search_kb("go gc") → Comparison
```

The agent's backstory instructs it to think step-by-step. It uses `search_kb` to look up each language before comparing, naturally exhibiting ReAct-style Thought → Action → Observation behavior.
