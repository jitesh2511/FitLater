'''
This module check for missing value diagnostics
per column and returns the issue if detected or 
returns None on no issue being detected
'''

from fitlater.diagnostics.base import make_issue, get_severity
from fitlater.config import MISSING_SEVERITY_THRESHOLD

def check_missing(column:str, profile:dict):

    missing_count = profile.get('missing_count', 0)
    missing_pct = profile.get('missing_pct', 0.0)
    
    # No issue is missing count is 0
    if missing_count == 0:
        return None

    missing_summary = {
        'missing_count': missing_count,
        'missing_pct': missing_pct,
    }
    severity = get_severity(missing_pct, MISSING_SEVERITY_THRESHOLD)
    return make_issue('missing', column, missing_summary, severity, True)
