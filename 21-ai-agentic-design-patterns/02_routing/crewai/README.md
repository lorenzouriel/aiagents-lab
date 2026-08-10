# Routing — CrewAI
A coordinator agent classifies incoming customer requests and routes them to the appropriate specialist agent (booking, info, or clarification).

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
python 02_routing/crewai/main.py
```

## How it works
```
Request → [Router Agent] → route_task → [Specialist Agent] → Response
```

A `router` agent classifies the request into a single category. The `handle_task` uses the routing decision (via `context=[route_task]`) to produce an appropriate response.
