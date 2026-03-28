from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import CORR_SEVERITY_THRESHOLD

def check_correlation(result) -> dict:
    correlation = result.get('correlation')

    if correlation.get('high_corr_pairs', None) is empty:
        return make_issue('correlation', None, False, "low")
    
    high_corr_pairs = correlation.get('high_corr_pairs', [])

    high_corr_summary = {}

    for idx, pair in enumerate(high_corr_pairs, 1):
        corr_value = pair.get('correlation', 0)
        # Severity assignment
        if abs(corr_value) <= CORR_SEVERITY_THRESHOLD['low']:
            severity = 'low'
        elif abs(corr_value) <= CORR_SEVERITY_THRESHOLD['medium']:
            severity = 'medium'
        else:
            severity = 'high'

        high_corr_summary[f'pair_{idx}'] = {
            'feature1': pair.get('feature_1'),
            'feature2': pair.get('feature_2'),
            'correlation': corr_value,
            'severity': severity,
            'hint': 'Merge both columns'
        }
    
    return make_issue('correlation', high_corr_summary, True, get_max_severity(high_corr_summary))