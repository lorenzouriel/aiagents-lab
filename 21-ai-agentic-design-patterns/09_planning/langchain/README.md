# Planning — LangChain
Demonstrates a plan-and-execute pattern: an LLM generates a numbered step-by-step plan, then a separate executor chain runs each step and reports its status.

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
python 09_planning/langchain/main.py
```

## How it works
```
Goal → [Planner Chain] → numbered plan
                              ↓
                   [Executor Chain × N steps] → status per step
```

The planner generates a structured plan. Simple line-based parsing extracts numbered steps, which are fed one at a time into the executor chain along with the full plan context for coherent responses.
