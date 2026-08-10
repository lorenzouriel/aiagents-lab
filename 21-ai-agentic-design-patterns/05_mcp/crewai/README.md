# Model Context Protocol (MCP) — CrewAI
An agent discovers available services from a simulated MCP registry and calls the appropriate tool, mirroring real MCP server discovery workflows.

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
python 05_mcp/crewai/main.py
```

## How it works
```
Task → [MCP Agent] → discover_services(query) → call_mcp_tool(service, tool, params) → Result
```

`MCP_REGISTRY` simulates a server directory. The agent uses `discover_services` to find matching services and `call_mcp_tool` to invoke them. In production, these would connect to real MCP endpoints via HTTP.
