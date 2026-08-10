# Human-in-the-Loop — CrewAI
A financial analyst agent prepares a trade recommendation and uses CrewAI's `human_input=True` flag to pause execution for human review before proceeding.

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
python 17_human_in_the_loop/crewai/main.py
```

> **Note:** This script pauses for human input during task execution.

## How it works
```
Task → [Analyst Agent] → Recommendation → [human_input=True] → ✓ Approved / ✗ Feedback
```

`human_input=True` on the task tells CrewAI to pause after the agent produces its output and prompt the user for approval or revision. If the human provides feedback, the agent can incorporate it before finishing.
