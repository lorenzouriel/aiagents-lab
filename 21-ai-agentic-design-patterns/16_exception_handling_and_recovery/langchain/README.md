# Exception Handling and Recovery — LangChain
Demonstrates retry logic with exponential backoff and graceful fallback. A simulated primary API fails twice before succeeding; on max retries, a secondary API is used instead.

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
python 16_exception_handling_and_recovery/langchain/main.py
```

## How it works
```
Query → resilient_fetch() → try primary_api (up to 3×, with 0.5s backoff)
                                       ↓ on max failure
                                 fallback_api() → [LLM Summary Chain] → Output
```

`resilient_fetch` wraps the primary API in a retry loop. If all retries fail it falls back to a cached data source. The LLM summary chain annotates the source reliability in its output.
