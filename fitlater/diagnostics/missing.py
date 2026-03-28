from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import MISSING_SEVERITY_THRESHOLD

def check_missing(result) -> dict:
    missing = result.get('missing')

    if missing is None:
        return make_issue('missing', None, False, "low")

    missing_per = missing.get('missing_percentage', {})

    missing_summary = {col : {'missing_percentage': missing_per[col],
                             'severity': 'low' if missing_per[col] <= MISSING_SEVERITY_THRESHOLD['low'] 
                              else 'medium' if missing_per[col] <= MISSING_SEVERITY_THRESHOLD['medium'] 
                              else 'high',
                             'hint': 'Impute missing values if important, else drop'}
                             for col in missing_per}
 
    return make_issue('missing', missing_summary, True, get_max_severity(missing_summary))
    
    