# Learning and Adaptation — LangChain
The agent reviews past campaign outcomes stored in an experience log, extracts key lessons, and designs an adapted strategy that avoids repeating past mistakes.

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
python 14_learning_and_adaptation/langchain/main.py
```

## How it works
```
experience_log → [Review Chain] → top 3 lessons → [Adapt Chain] → Improved Strategy
```

`experience_log` simulates historical memory. The `review_chain` distills lessons from past results; the `adapt_chain` uses those lessons to design the next campaign — never repeating identified mistakes.
