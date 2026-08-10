# Inter-Agent Communication (A2A) — CrewAI
A coordinator agent discovers remote agents via simulated A2A Agent Cards and delegates tasks to them (weather check + flight booking) using the A2A protocol.

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
python 07_inter_agent_communication_a2a/crewai/main.py
```

## How it works
```
Task → [Coordinator Agent] → discover_agents(query) → send_a2a_task(url, skill, params) → Results
```

`AGENT_CARDS` simulates the A2A discovery registry. The coordinator uses `discover_agents` to find agents by capability and `send_a2a_task` to invoke them over the A2A JSON-RPC protocol.
