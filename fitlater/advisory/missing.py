from fitlater.advisory.util import build_advice
from fitlater.advisory.strategies import get_imputation_strategy

def handle_missing(profile:dict, diag:dict) -> dict:

    column = diag["column"]
    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    missing_pct = data["details"]["missing_pct"]

    if severity == "high":
        action = "Drop column"
        reason = f"Too many missing values ({missing_pct}%)"
        priority = 1

    elif severity == 'medium':
        strategy = get_imputation_strategy(profile[column])

        if strategy == "median":
            action = "Fill with median"
            reason = "Robust to skewed data"

        elif strategy == "mode":
            action = "Fill with mode"
            reason = "Suitable for categorical data"

        else:
            action = "Fill with mean"
            reason = "Suitable for normal distributions"

        priority = 2
    
    else:
        action = "No immediate action required"
        reason = f"Missing values are minimal ({missing_pct}%) and unlikely to impact modeling"
        priority = 3

    return build_advice(column, "missing", action, reason, priority)
