# Planning — CrewAI
A planning agent decomposes a high-level goal into a step-by-step plan, then an executor agent carries out each step and reports completion.

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
python 09_planning/crewai/main.py
```

## How it works
```
Goal → [Planner Agent] → plan → [Executor Agent] → Step-by-step Report
```

The `plan_task` defines the goal and asks for a numbered, budgeted plan. The `execute_task` uses `context=[plan_task]` to receive the plan and walks through each step sequentially.
