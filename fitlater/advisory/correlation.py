"""
This module provides advisory logic for handling highly correlated columns in a dataset.
When two features are strongly correlated, they may offer redundant information, impacting
model interpretability and potentially causing multicollinearity issues. This module's
core function inspects column correlations and generates appropriate advice, including
recommendations to drop or further investigate correlated features based on correlation
strength, for use in automated data diagnostics.
"""

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