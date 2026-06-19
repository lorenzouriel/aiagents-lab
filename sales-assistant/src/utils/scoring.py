from src.graph.state import ConversationState


def compute_temperature(state: ConversationState) -> str:
    profile = state.get("lead_profile", {})
    score = 0

    if profile.get("urgency") == "high":
        score += 3
    elif profile.get("urgency") == "medium":
        score += 1

    if profile.get("budget_signal"):
        score += 2

    if profile.get("product_interest"):
        score += 2

    # Rewarded for re-engaging after follow-up
    if state.get("follow_up_scheduled") and state.get("turn_count", 0) > 1:
        score += 2

    # Penalise unresolved objections
    score -= len(state.get("objections_raised", []))

    if score >= 5:
        return "hot"
    if score >= 2:
        return "warm"
    return "cold"
