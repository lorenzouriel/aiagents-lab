# Tool Use — LangChain
Demonstrates function calling with LangChain tools. An LLM is bound to custom tools (`get_weather`, `calculate`) and runs a ReAct-style loop to invoke them.

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
python 04_tool_use/langchain/main.py
```

## How it works
```
Query → [LLM + Tools] → tool_call → [Tool Executor] → ToolMessage → [LLM] → Answer
```

`llm.bind_tools(tools)` exposes the tools to the model. The agent loop runs up to 5 iterations: if the model returns tool calls, they are executed and results appended as `ToolMessage`s; otherwise the loop exits with the final answer.
