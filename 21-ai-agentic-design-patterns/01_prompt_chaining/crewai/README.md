# Prompt Chaining — CrewAI
Demonstrates sequential task decomposition using CrewAI. A market report is summarized, trends are extracted, and an executive email is drafted — each agent receiving the previous task's output via `context`.

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
python 01_prompt_chaining/crewai/main.py
```

## How it works
```
Report → [Summarizer Agent] → [Trend Analyst Agent] → [Email Writer Agent]
```

Three agents run sequentially (`Process.sequential`). Each task passes its output to the next via `context=[previous_task]`.