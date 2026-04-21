'''
This module check for outlier value diagnostics
per column and returns the issue if detected or 
returns None on no issue being detected
'''

import pandas as pd

from fitlater.diagnostics.base import get_severity, make_issue
from fitlater.config import OUTLIER_SEVERITY_THRESHOLD

def check_outliers(column:str, profile:dict, data:pd.Series):

    # No issue if column is not numeric
    if not profile.get('type') == 'numeric':
        return None

    q1 = profile.get('q1')
    q3 = profile.get('q3')
    iqr = q3 - q1
    lb = q1 - (iqr * 1.5)
    ub = q3 + (iqr * 1.5)

    outlier_count = int(((data < lb) | (data > ub)).sum(skipna=True))
    outlier_pct = round((outlier_count / len(data.dropna()) * 100), 2)

    # No issue if outlier count is 0
    if outlier_count == 0:
        return None

    outliers_summary = {
        'outlier_count': outlier_count,
        'outlier_pct': outlier_pct,
    }
    severity= get_severity(outlier_pct, OUTLIER_SEVERITY_THRESHOLD)

    return make_issue('outliers', column, outliers_summary, severity, True)