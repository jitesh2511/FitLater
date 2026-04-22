import pandas as pd

from fitlater.diagnostics.base import make_issue, get_severity
from fitlater.config import DUPLICATE_THRESHOLD

def check_duplicates(profile:dict, df:pd.DataFrame) -> dict | None:

    total_rows = len(df)

    if total_rows == 0:
        return None

    dup_count = df.duplicated().sum()

    if dup_count == 0:
        return None

    dup_ratio = dup_count / total_rows
    dup_pct = round(dup_ratio * 100, 2)
    severity = get_severity(dup_pct, DUPLICATE_THRESHOLD)

    return make_issue(
        "duplicates",
        "dataset",
        {
            "issue_type": "duplicate_rows",
            "expected_type": "unique_rows",
            "current_type": "duplicate_present",
            "confidence": round(dup_ratio, 2),
            "details": {
                "duplicate_count": int(dup_count),
                "duplicate_pct": dup_pct
            }
        },
        severity,
        True
    )