'''
This module check for correlation value diagnostics
for all columns and returns the list of columns with
problems if detected any else returns an empty list
'''


import pandas as pd
from fitlater.diagnostics.base import get_severity, make_issue
from fitlater.config import CORRELATION_THRESHOLD, CORR_SEVERITY_THRESHOLD

def check_correlation_all(profiles: dict, df: pd.DataFrame) -> list:
    diagnostics = []
    numeric_cols = [col for col, p in profiles.items() if p.get('type') == 'numeric']

    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            issue = get_correlation_diag(
                {
                    'column': col1,
                    'profile': profiles[col1],
                    'data': df[col1]
                },
                {
                    'column': col2,
                    'profile': profiles[col2],
                    'data': df[col2]
                }
            )

            if issue:
                diagnostics.append(issue)

    return diagnostics  

def get_correlation_diag(column_1_meta:dict, column_2_meta:dict):

    column_1 = column_1_meta.get('column')
    column_2 = column_2_meta.get('column')
    columns = {
        'column_1': column_1,
        'column_2': column_2
    }
    
    profile_1 = column_1_meta.get('profile')
    data_1 = column_1_meta.get('data')
    profile_2 = column_2_meta.get('profile')
    data_2 = column_2_meta.get('data')
    
    # No issue if both columns are not numeric
    if not profile_1.get('type') == 'numeric' and not profile_2.get('type') == 'numeric':
        return None
    
    corr = data_1.corr(data_2)

    # In case of constant columns or insufficient data
    if pd.isna(corr):
        return None

    high_corr = abs(corr) > CORRELATION_THRESHOLD

    # No issue if correlation is less than the defined threshold
    if not high_corr:
        return None

    # Severity assignment
    severity = get_severity(abs(corr), CORR_SEVERITY_THRESHOLD)

    high_corr_summary = {
        'correlation': round(corr, 4),
    }
    
    return make_issue('corr', columns, high_corr_summary, severity, True)