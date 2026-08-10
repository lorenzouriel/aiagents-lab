# Exploration and Discovery — CrewAI
Three agents explore drug discovery from different angles: an explorer generates hypotheses, a critic evaluates them, and a synthesizer combines the best into a research proposal.

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
python 15_exploration_and_discovery/crewai/main.py
```

## How it works
```
[Explorer] → hypotheses → [Critic] → evaluation → [Synthesizer] → Research Proposal
```

`t2` (critic) receives `context=[t1]` and `t3` (synthesizer) receives `context=[t1, t2]`, so the synthesizer sees both the original hypotheses and the critical evaluation when forming the final proposal.
