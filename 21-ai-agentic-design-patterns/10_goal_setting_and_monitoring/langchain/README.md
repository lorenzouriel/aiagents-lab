# Goal Setting and Monitoring — LangChain
Demonstrates goal definition, execution tracking, and progress monitoring. An LLM defines SMART goals, simulates week-1 execution, and a monitor identifies risks and recommends adjustments.

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
python 10_goal_setting_and_monitoring/langchain/main.py
```

## How it works
```
Objective → [Goal Chain] → SMART Goals
                              ↓
                         [Execute Chain] → Progress Metrics
                              ↓
                         [Monitor Chain] → Risk Report + Recommendations
```

Three specialized chains form a feedback loop: goal-setting → execution simulation → monitoring. The monitor receives both the original goals and the progress report to produce corrective recommendations.
