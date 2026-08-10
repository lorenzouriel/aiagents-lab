# Prioritization — LangChain
Scores tasks using a weighted formula (urgency × 0.5 + importance × 0.3 + dependency bonus × 0.2), ranks them, and uses an LLM to generate natural-language justification for each ranking.

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
python 20_prioritization/langchain/main.py
```

## How it works
```
tasks[] → score_task() → sorted list (P0→P4)
                              ↓
                   [justify_chain] → "Why this priority?" → Final ranked output
```

`score_task` computes a numeric priority score. Tasks are sorted descending and labeled P0–P4. The `justify_chain` generates a concise 1–2 sentence rationale for each ranking, enriching the output for a human reader.
