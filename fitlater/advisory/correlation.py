from fitlater.advisory.util import build_advice

def handle_corr(profile:dict, diag:dict) -> dict | None:

    columns = diag["column"]
    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    f1 = columns["column_1"]
    f2 = columns["column_2"]

    corr = abs(data["details"]["correlation"])

    if severity == "high":
        action = "Drop one of the correlated columns"
        reason = f"Very high correlation ({corr})"
        priority = 1

    elif severity == 'medium':
        action = "Consider feature selection"
        reason = f"Moderate correlation ({corr})"
        priority = 2

    else:
        action = "No action required"
        reason = f"Low correlation between features ({corr}) does not indicate redundancy"
        priority = 3
        
    column = f"{f1} & {f2}"

    return build_advice(column, "correlation", action, reason, priority)