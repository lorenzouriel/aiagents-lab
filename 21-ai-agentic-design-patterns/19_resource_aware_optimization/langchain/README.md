# Resource-Aware Optimization — LangChain
Dynamic model selection based on query complexity. Simple queries are routed to a fast/cheap model; complex analytical queries go to a premium model — optimizing cost and latency.

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
python 19_resource_aware_optimization/langchain/main.py
```

## How it works
```
Query → assess_complexity() → "simple" | "complex"
                                    ↓
                           models[complexity] → [Prompt | LLM | Parser] → Answer
```

`assess_complexity` uses word count and keyword detection to classify the query. The selected model is then used to build and run the chain, keeping costs proportional to query difficulty.
