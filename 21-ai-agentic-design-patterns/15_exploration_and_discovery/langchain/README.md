# Exploration and Discovery — LangChain
A Generate-Debate-Evolve loop: the system generates hypotheses, critiques them, and evolves stronger versions — iterating for configurable cycles to discover novel insights.

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
python 15_exploration_and_discovery/langchain/main.py
```

## How it works
```
Topic → [Generator] → hypotheses
                          ↓  (× cycles)
                      [Critic] → critique → [Evolver] → stronger hypotheses
```

Each cycle passes the current hypotheses to the critic, then to the evolver with both the original and the critique. After `cycles` iterations, the final evolved hypotheses are returned.
