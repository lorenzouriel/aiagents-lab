# Reflection — CrewAI
Producer-Critic model: a writer drafts content, a critic evaluates it, and a refiner produces an improved version — demonstrating one-shot reflection with CrewAI's sequential task flow.

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
python 08_reflection/crewai/main.py
```

## How it works
```
[Producer] → draft → [Critic] → feedback → [Refiner] → Final Output
```

Three tasks chain sequentially: `task_critique` receives `context=[task_draft]`, and `task_refine` receives `context=[task_draft, task_critique]` so the refiner can see both the original and the feedback.
