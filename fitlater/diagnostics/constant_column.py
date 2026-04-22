import pandas as pd
from fitlater.diagnostics.base import make_issue

def check_constant(column: str, profile: dict, data:pd.Series) -> dict | None:
    
    n_unique = profile.get("n_unique", 0)

    if n_unique != 1:
        return None

    return make_issue(
        "constant",
        column,
        {
            "issue_type": "constant_column",
            "expected_type": "variable",
            "current_type": profile.get("type"),
            "confidence": 1.0,
            "details": {}
        },
        "high",
        True
    )