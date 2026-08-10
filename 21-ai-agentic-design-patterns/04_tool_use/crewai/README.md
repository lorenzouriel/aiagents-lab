# Tool Use — CrewAI
An agent is equipped with custom tools (`get_weather`, `calculate`) to fetch weather data and perform calculations, deciding when and how to call them autonomously.

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
python 04_tool_use/crewai/main.py
```

## How it works
```
Task → [Travel Assistant Agent] → get_weather() / calculate() → Answer
```

Tools are registered on the agent via `tools=[get_weather, calculate]`. CrewAI handles the tool-call loop internally — the agent decides when to call each tool and synthesizes the results into a final recommendation.
