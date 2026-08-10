# Reflection — LangChain
Implements a Producer-Critic reflection loop that iteratively improves technical content. The producer drafts, the critic reviews, and the refiner incorporates feedback — repeated for `N` iterations.

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
python 08_reflection/langchain/main.py
```

## How it works
```
Instruction → [Producer] → draft
                               ↓
                          [Critic] → feedback
                               ↓
                          [Refiner] → improved draft → (repeat N times)
```

Each iteration passes the current draft to the critic and then refines it with the resulting feedback. The final refined draft is returned as output.
