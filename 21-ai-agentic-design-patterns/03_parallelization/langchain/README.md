# Parallelization — LangChain
Uses `RunnableParallel` to execute three independent research chains concurrently, then synthesizes all results in a final chain.

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
python 03_parallelization/langchain/main.py
```

## How it works
```
           ┌─ [AI Research Chain]     ─┐
Input ─────┤─ [Energy Research Chain] ─┼──→ [Synthesis Chain] → Report
           └─ [EV Research Chain]     ─┘
```

`RunnableParallel` fans out to three chains simultaneously. Their outputs are passed as a dict to the synthesis chain, which merges them into a single executive brief.
