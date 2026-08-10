# Advanced Reasoning — LangChain
Demonstrates two reasoning strategies: Chain-of-Thought (CoT) prompting for structured step-by-step answers, and a simplified ReAct loop that alternates between thinking, acting, and observing.

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
python 11_advanced_reasoning/langchain/main.py
```

## How it works
```
CoT:   Question → [Step-by-step prompt] → Reasoned Answer

ReAct: Question → Thought → KB lookup (Observation) → Thought → ... → CONCLUDE → Final Answer
```

The CoT chain uses a system prompt that enforces `Step N: [reasoning]... Conclusion:` format. The ReAct loop checks for a `CONCLUDE` signal and breaks early, then synthesizes the full reasoning trace into a final answer.
