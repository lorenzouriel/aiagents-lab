# Multi-Agent Collaboration — LangChain
Three specialized chains (Researcher → Writer → Editor) collaborate in a sequential pipeline to produce a polished blog post.

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
python 06_multi_agent_collaboration/langchain/main.py
```

## How it works
```
Topic → [Researcher Chain] → [Writer Chain] → [Editor Chain] → Final Post
```

Each chain specializes in one role. The output of each step is explicitly passed as input to the next, forming a handoff pipeline where every agent builds on the previous one's work.
