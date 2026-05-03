"""
Detect constant columns.

Provides `check_constant()` which returns a diagnostic issue when a
column contains only a single unique (non-null) value. Such columns
are generally unhelpful for modeling and are flagged as high severity.
"""

import pandas as pd
from fitlater.diagnostics.base import make_issue


def check_constant(column: str, profile: dict, data:pd.Series) -> dict | None:

    n_unique = data.dropna().nunique()

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