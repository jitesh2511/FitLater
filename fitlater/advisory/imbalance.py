from fitlater.advisory.util import build_advice

def handle_imbalance(profile:dict, diag:dict) -> dict | None:

    column = diag["column"]
    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    dominance = data["details"]["dominance_ratio"]

    if not isinstance(dominance, (int, float)):
        return None

    if severity == "high":
        action = "Consider resampling (SMOTE, undersampling)"
        reason = f"Severe class imbalance detected ({dominance*100:.1f}% dominance)"
        priority = 1

    elif severity == "medium":
        action = "Monitor imbalance or use class weights"
        reason = f"Moderate imbalance may affect model performance ({dominance*100:.1f}% dominance)"
        priority = 2

    else:
        action = "No action required"
        reason = f"Class distribution is reasonably balanced ({dominance*100:.1f}% dominance)"
        priority = 3

    return build_advice(column, "imbalance", action, reason, priority)