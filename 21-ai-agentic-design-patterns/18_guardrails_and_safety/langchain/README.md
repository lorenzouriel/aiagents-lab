# Guardrails and Safety — LangChain
Multi-layer safety pipeline: input validation via regex patterns, behavioral constraints in the system prompt, and output filtering to redact PII before delivery.

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
python 18_guardrails_and_safety/langchain/main.py
```

## How it works
```
Input → [Layer 1: validate_input()] → blocked? → return warning
                ↓ safe
         [Layer 2: LLM + safety system prompt] → raw output
                ↓
         [Layer 3: filter_output()] → PII redacted → Final Response
```

Three layers work in sequence: regex blocks prohibited phrases before the LLM sees the input; the system prompt enforces behavioral rules; `filter_output` scrubs SSN/credit-card patterns from the response.
