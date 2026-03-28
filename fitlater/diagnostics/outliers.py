from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import OUTLIER_SEVERITY_THRESHOLD

def check_outliers(result) -> dict:
    outliers = result.get('outliers')

    if outliers.get('outlier_summary', None) is None:
        return make_issue('outliers', None, False, "low")
    
    outliers_per = outliers.get('outlier_percentage', {})

    outliers_summary = {col : {
        'outlier_percentage': outliers_per[col],
        'severity': 'low' if outliers_per[col] <= OUTLIER_SEVERITY_THRESHOLD['low'] 
        else 'medium' if outliers_per[col] <= OUTLIER_SEVERITY_THRESHOLD['medium'] 
        else 'high',
        'hint': 'Impute outliers if important, else drop'
    } for col in outliers_per}

    return make_issue('outliers', outliers_summary, True, get_max_severity(outlier_summary))