# Resource-Aware Optimization — CrewAI
A router agent assesses query complexity using a tool and reports which model tier (simple / moderate / complex) should handle it, enabling cost-aware task routing.

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
python 19_resource_aware_optimization/crewai/main.py
```

## How it works
```
Query → [Router Agent] → assess_complexity(query) → "simple" | "moderate" | "complex"
                                                          ↓
                                               Model tier recommendation + justification
```

`assess_complexity` classifies queries by word count and analytical keywords. The router agent calls it first, then explains which model tier is appropriate and why — suitable for routing logic in a larger multi-agent system.
