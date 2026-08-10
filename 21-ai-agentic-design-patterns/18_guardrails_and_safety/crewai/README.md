# Guardrails and Safety — CrewAI
An agent validates every user input through an `Input Validator` tool before responding, blocking prohibited topics and enforcing safety rules inside its backstory.

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
python 18_guardrails_and_safety/crewai/main.py
```

## How it works
```
Request → [Safe Agent] → validate_input(message) → "safe" / "blocked: reason"
                                    ↓ safe
                           [Agent responds with safety-constrained output]
```

`validate_input` checks the message against `BLOCKED_TOPICS` and enforces a length limit. The agent's backstory requires it to always call the validator first, and to refuse if the result is anything other than `"safe"`.
