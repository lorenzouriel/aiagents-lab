# Multi-Agent Collaboration — CrewAI
A team of three specialized agents (Researcher → Writer → Editor) collaborates to produce a publication-ready blog post via sequential task handoffs.

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
python 06_multi_agent_collaboration/crewai/main.py
```

## How it works
```
[Researcher] → [Writer] → [Editor] → Final Post
```

Each agent handles exactly one task. Context flows via `context=[previous_task]` in each `Task` definition, giving every agent full visibility of prior outputs.
