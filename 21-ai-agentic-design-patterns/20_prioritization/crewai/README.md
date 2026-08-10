# Prioritization — CrewAI
A prioritization specialist agent receives a list of tasks and ranks them P0–P4 based on urgency, business impact, and dependency analysis.

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
python 20_prioritization/crewai/main.py
```

## How it works
```
Task list → [Prioritizer Agent] → P0: critical bug, P1: payment feature, ... → Ranked Output
```

The task description embeds the full input list and asks for P0–P4 ratings with justification. The agent applies its expertise in urgency, impact, and dependency analysis to produce a prioritized work order.
