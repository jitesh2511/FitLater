import pandas as pd

from fitlater.diagnostics.base import make_issue
from fitlater.config import NUMERIC_RATIO_THRESHOLD, DATETIME_RATIO_THRESHOLD, MIXED_NUMERIC_THRESHOLD, BOOLEAN_SETS

def check_type_issues(column:str, profile:dict, data:pd.Series) -> dict | None:

    series = data.dropna()

    if len(series) == 0:
        return None
    
    if profile.get('type') == 'categorical':
        return check_categorical_conversion(column, series)

    return None

def check_categorical_conversion(column: str, data:pd.Series):

    # Numeric
    numeric_conv = pd.to_numeric(data, errors='coerce')
    numeric_ratio = numeric_conv.notna().mean()

    if numeric_ratio > NUMERIC_RATIO_THRESHOLD:
        return make_issue(
            'type_issue',
            column,
            {
                "expected_type": "numeric",
                "current_type": "categorical",
                "issue_type": "numeric_as_string",
                "confidence": round(numeric_ratio, 2),
                "details": {
                    "convertible_pct": round(numeric_ratio * 100, 2)
                }
            },
            'high',
            True
        )
    
    # DateTime
    datetime_conv = pd.to_datetime(data, errors='coerce', format='mixed')
    datetime_ratio = datetime_conv.notna().mean()

    if datetime_ratio > DATETIME_RATIO_THRESHOLD:
        return make_issue(
            'type_issue',
            column,
            {
                "expected_type": "datetime",
                "current_type": "categorical",
                "issue_type": "datetime_as_string",
                "confidence": round(datetime_ratio, 2),
                "details": {
                    "convertible_pct": round(datetime_ratio * 100, 2)
                }
            },
            'high',
            True
        )

    # Boolean
    unique_values = set(data.astype(str).str.strip().str.lower().unique())
    
    if len(unique_values) > 1 and any(unique_values <= bset for bset in BOOLEAN_SETS):
        return make_issue(
            'type_issue',
            column,
            {
                "expected_type": "boolean",
                "current_type": "categorical",
                "issue_type": "boolean_as_string",
                "confidence": 1.0,
                "details": {
                    "values": list(unique_values)
                }
            },
            'medium',
            True
        )
    
    # Mixed numeric
    if MIXED_NUMERIC_THRESHOLD[0] < numeric_ratio < MIXED_NUMERIC_THRESHOLD[1]:
        return make_issue(
            "type_issue",
            column,
            {
                "expected_type": "numeric",
                "current_type": "categorical",
                "issue_type": "mixed_types",
                "confidence": round(numeric_ratio, 2),
                "details": {
                    "numeric_convertible_pct": round(numeric_ratio * 100, 2)
                }
            },
            "medium",
            True
        )

    return None