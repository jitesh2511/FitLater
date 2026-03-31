from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import OUTLIER_SEVERITY_THRESHOLD

def check_outliers(outliers) -> dict:
    
    if outliers.get('outlier_summary', None) is None:
        return make_issue('outliers', None, False, "low")
    
    outliers_per = outliers.get('outlier_percentage', {})

    valid_outliers = {col : outliers_per[col] for col in outliers_per.keys() if abs(outliers_per[col]) > 1e-12}

    if not valid_outliers:
        return make_issue('outliers', None, False, 'low')

    outliers_summary = {col : {
        'outlier_percentage': valid_outliers[col],
        'severity': 'low' if valid_outliers[col] <= OUTLIER_SEVERITY_THRESHOLD['low'] 
        else 'medium' if valid_outliers[col] <= OUTLIER_SEVERITY_THRESHOLD['medium'] 
        else 'high',
        'hint': 'Impute outliers if important, else drop'
    } for col in valid_outliers}

    return make_issue('outliers', outliers_summary, True, get_max_severity(outliers_summary))