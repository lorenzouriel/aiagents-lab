# Inter-Agent Communication (A2A) — LangChain
Simulates the Agent-to-Agent (A2A) protocol: Agent Cards, skill-based discovery, and standardized task delegation between independent agent services.

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
python 07_inter_agent_communication_a2a/langchain/main.py
```

## How it works
```
Coordinator → a2a_discover(server) → Agent Card → a2a_send_task(server, skill, params) → Result
```

`A2AServer` simulates compliant agent services with `get_agent_card()` (`/.well-known/agent.json`) and `send_task()` (JSON-RPC). A coordinator discovers available skills and delegates tasks across services — no LLM call needed, showing the pure protocol layer.
