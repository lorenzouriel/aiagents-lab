# Goal Setting and Monitoring — CrewAI
Three agents set SMART goals, simulate execution, and monitor progress — identifying at-risk goals and recommending course corrections.

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
python 10_goal_setting_and_monitoring/crewai/main.py
```

## How it works
```
[Goal Strategist] → SMART Goals → [Task Executor] → Progress → [Progress Monitor] → Report
```

`task_monitor` uses `context=[task_goals, task_execute]` to simultaneously access the defined goals and the week-1 progress, enabling accurate deviation detection and adjustment recommendations.
