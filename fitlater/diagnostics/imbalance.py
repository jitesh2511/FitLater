import pandas as pd

from fitlater.diagnostics.base import get_severity, make_issue
from fitlater.config import IMBALANCE_THRESHOLDS

def check_imbalance(column: str, profile: dict, data:pd.Series) -> dict | None:

    if profile.get("type") != "categorical":
        return None

    top_freq = profile.get("top_freq", 0)
    total_rows = len(data)
    if total_rows == 0:
        return None

    dominance = top_freq / total_rows

    severity = get_severity(dominance, IMBALANCE_THRESHOLDS)

    if severity == 'low':
        return None

    return make_issue(
        "imbalance",
        column,
        {
            "issue_type": "imbalanced_category",
            "expected_type": "balanced",
            "current_type": "categorical",
            "confidence": round(dominance, 2),
            "details": {
                "dominance_ratio": round(dominance, 2)
            }
        },
        severity,
        True
    )