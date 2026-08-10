# Parallelization — CrewAI
Three independent research agents work concurrently on different topics. A synthesis agent merges their findings into a unified executive brief.

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
python 03_parallelization/crewai/main.py
```

## How it works
```
[AI Researcher] ──┐
[Energy Researcher] ──┼──→ [Synthesizer Agent] → Unified Brief
[EV Researcher] ──┘
```

The three research tasks have no dependencies on each other. The synthesis task uses `context=[task_ai, task_energy, task_ev]` to receive all three outputs and merge them.
