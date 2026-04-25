from fitlater.advisory.util import build_advice

def handle_distribution(profile:dict, diag:dict) -> dict | None:

    column = diag["column"]
    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    skew = data["details"]["skew"]

    if severity == "high":
        action = "Apply log or Box-Cox transformation"
        reason = f"Highly skewed data can negatively impact model performance (skew={skew})"
        priority = 1

    elif severity == "medium":
        action = "Consider transformation if model is sensitive"
        reason = f"Moderate skewness may affect some models (skew={skew})"
        priority = 2

    else:
        action = "No immediate action required"
        reason = f"Low skew ({skew}) is unlikely to affect most models"
        priority = 3


    return build_advice(column, "distribution", action, reason, priority)