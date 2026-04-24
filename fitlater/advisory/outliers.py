from fitlater.advisory.util import build_advice

def handle_outliers(profile:dict, diag:dict) -> dict | None:

    column = diag["column"]
    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    outlier_pct = data["details"]["outlier_pct"]

    if severity == "high":
        action = "Investigate data or consider dropping column"
        reason = f"High percentage of outliers ({outlier_pct}%) may indicate data issues"
        priority = 1

    elif severity == "medium":
        action = "Apply capping or transformation"
        reason = f"Moderate outliers may distort model performance ({outlier_pct}%)"
        priority = 2

    else:
        action = "No immediate action required"
        reason = f"Low percentage of outliers ({outlier_pct}%) is unlikely to impact model performance"
        priority = 3

    return build_advice(column, "outliers", action, reason, priority)