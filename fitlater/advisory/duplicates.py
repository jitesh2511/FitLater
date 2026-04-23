from fitlater.advisory.util import build_advice

def handle_duplicates(profile:dict, diag:dict) -> dict | None:

    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    dup_pct = data["details"]["duplicate_pct"]

    if severity == "high":
        action = "Remove duplicate rows immediately"
        reason = f"High duplicate percentage ({dup_pct}%) can bias model training"
        priority = 1

    elif severity == "medium":
        action = "Consider removing duplicate rows"
        reason = f"Moderate duplicate percentage ({dup_pct}%) may affect results"
        priority = 2

    else:
        return None

    return build_advice("dataset", "duplicates", action, reason, priority)