# Evaluation and Monitoring — LangChain
LLM-as-a-Judge: a customer support response is generated, then a separate evaluator LLM scores it on accuracy, completeness, helpfulness, and clarity — returning structured JSON scores.

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
python 21_evaluation_and_monitoring/langchain/main.py
```

## How it works
```
Question → [Response Chain] → answer
                                  ↓
                         [Eval Chain] → JSON scores {accuracy, completeness, helpfulness, clarity, overall, feedback}
```

The evaluator is prompted to return **only** valid JSON. The output is parsed with `json.loads`; if parsing fails the raw output is preserved. This pattern enables automated quality gates in production pipelines.
