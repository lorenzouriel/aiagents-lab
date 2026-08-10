# Learning and Adaptation — CrewAI
An adaptive content strategist reviews past campaign performance data, extracts lessons, and designs an improved strategy for the next quarter.

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
python 14_learning_and_adaptation/crewai/main.py
```

## How it works
```
Past Results → [Learner Agent: review] → lessons → [Learner Agent: adapt] → Adapted Strategy
```

A single agent handles both tasks. `task_adapt` uses `context=[task_review]` so the adaptation step receives the extracted lessons directly, ensuring the new strategy explicitly addresses what went wrong.
