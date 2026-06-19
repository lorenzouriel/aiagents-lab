import re


def extract_lead_signals(text: str) -> dict:
    """Extract qualification signals from agent or user message text."""
    signals: dict = {}
    lower = text.lower()

    # Budget signals (BRL)
    budget_match = re.search(r"r\$\s*(\d[\d.,]*)", lower)
    if budget_match:
        signals["budget_signal"] = budget_match.group(0).strip()

    # Urgency signals
    urgent_keywords = ["urgente", "hoje", "amanhã", "logo", "rápido", "essa semana", "preciso já"]
    low_keywords = ["sem pressa", "pensando", "futuramente", "talvez"]
    if any(k in lower for k in urgent_keywords):
        signals["urgency"] = "high"
    elif any(k in lower for k in low_keywords):
        signals["urgency"] = "low"

    # Name extraction (simple heuristic: "me chamo X" / "meu nome é X")
    name_match = re.search(r"(?:me chamo|meu nome é|sou (?:a |o )?)\s*([A-ZÀ-Ú][a-zà-ú]+)", text)
    if name_match:
        signals["name"] = name_match.group(1)

    return signals
