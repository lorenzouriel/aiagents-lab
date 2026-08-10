# Human-in-the-Loop — LangChain
An agent prepares a trade recommendation, then pauses at a human approval gate. The trade executes only if the human confirms; otherwise it is cancelled.

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
python 17_human_in_the_loop/langchain/main.py
```

> **Note:** This script prompts for `yes/no` input at the terminal.

## How it works
```
Ticker + Price → [Analyst Chain] → Recommendation
                                        ↓
                              human_approval_gate() → yes → execute_trade()
                                                    → no  → cancelled
```

`human_approval_gate` prints the recommendation and blocks on `input()`. Only a `yes`/`y` response triggers `execute_trade()`.
