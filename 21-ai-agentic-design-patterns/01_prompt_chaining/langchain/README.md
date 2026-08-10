# Prompt Chaining — LangChain
Demonstrates sequential prompt chaining using LCEL (LangChain Expression Language). A market report is summarized, trends are extracted, and an executive email is drafted — each step feeding into the next.

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
python 01_prompt_chaining/langchain/main.py
```

## How it works
```
Report → [Summarize] → [Extract Trends] → [Draft Email]
```

Each step is a `ChatPromptTemplate` chained with `|` using LCEL. The output of one prompt becomes the input of the next.