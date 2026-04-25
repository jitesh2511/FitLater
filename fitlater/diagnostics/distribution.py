'''
This module check for skew value diagnostics
per column and returns the issue if detected or 
returns None on no issue being detected
'''


import pandas as pd

from fitlater.diagnostics.base import get_severity, make_issue
from fitlater.config import SKEW_THRESHOLD, SKEW_SEVERITY_THRESHOLD

def check_distribution(column:str, profile:dict, data:pd.Series) -> dict | None:

    # No issue if the column is not numeric
    if not profile.get('type') == 'numeric':
        return None

    skew = profile.get('skew')

    if skew is None:
        return None

    high_skew = abs(skew) > SKEW_THRESHOLD

    # No issue if skew is not greater than the define threshold
    if not high_skew:
        return None

    skew_summary = {
        'issue_type': 'skewed_column',
        'expected_type': 'low_skew',
        'current_type': 'high_skew',
        'confidence': round(abs(skew), 2),
        'details': {
            'skew' : round(skew, 4),
            'kurt' : round(profile.get('kurt'), 4)
        }
    }
    severity = get_severity(abs(skew), SKEW_SEVERITY_THRESHOLD)

    return make_issue('distribution', column, skew_summary, severity, True)