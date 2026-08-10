# Exception Handling and Recovery — CrewAI
A resilient agent attempts the primary data API first and automatically falls back to a secondary cached source if the primary fails — reporting which data source was used.

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
python 16_exception_handling_and_recovery/crewai/main.py
```

## How it works
```
Task → [Resilient Agent] → primary_api() → fails → fallback_api() → Result with source attribution
```

`primary_api` raises an exception on the first call to simulate a transient failure. The agent's backstory instructs it to always try the primary first and use the fallback if it fails, demonstrating tool-level recovery logic.
