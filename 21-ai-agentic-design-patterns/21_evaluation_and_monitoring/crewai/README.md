# Evaluation and Monitoring — CrewAI
A QA evaluator agent reviews the customer support agent's response and scores it on four quality dimensions: accuracy, completeness, helpfulness, and clarity.

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
python 21_evaluation_and_monitoring/crewai/main.py
```

## How it works
```
[Support Agent] → answer → [QA Evaluator Agent] → scores (1–5) + improvement feedback
```

`task_evaluate` uses `context=[task_respond]` to receive the support agent's answer. The evaluator scores each dimension 1–5 and provides actionable feedback, simulating a continuous quality monitoring loop.
