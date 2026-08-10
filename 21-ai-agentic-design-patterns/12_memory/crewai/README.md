# Memory — CrewAI
Demonstrates CrewAI's built-in memory system. A single assistant agent handles a multi-turn conversation, retaining context across tasks via `memory=True` at the crew level.

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
python 12_memory/crewai/main.py
```

## How it works
```
task1 (introduce) → task2 (context=[task1], ask role) → task3 (context=[task1,task2], recall)
```

`memory=True` enables CrewAI's short-term and long-term memory stores. Explicit `context=[...]` references also ensure each task can access prior outputs directly, creating two overlapping memory mechanisms.
