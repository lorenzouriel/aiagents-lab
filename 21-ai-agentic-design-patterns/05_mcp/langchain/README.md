# Model Context Protocol (MCP) — LangChain
Demonstrates MCP-style dynamic tool discovery and invocation. Tools are registered in a simulated MCP server and discovered at runtime by the agent.

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
python 05_mcp/langchain/main.py
```

## How it works
```
Query → [Agent] → mcp_discover(server) → tool list → mcp_invoke(server, tool, params) → Result
```

The `MCPServer` class simulates a server with a `discover()` endpoint and an `invoke()` dispatcher. Two LangChain tools wrap these: `mcp_discover` and `mcp_invoke`. The agent finds available tools at runtime before calling them.
