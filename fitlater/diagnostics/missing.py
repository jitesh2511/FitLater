from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import MISSING_SEVERITY_THRESHOLD

def check_missing(result) -> dict:
    missing = result.get('missing')

    if missing is None:
        return make_issue('missing', {}, False, "low")

    missing_per = missing.get('missing_percentage', {})

    valid_missing = {col: missing_per[col] for col in missing_per if abs(missing_per[col]) > 1e-12}

    if not valid_missing:
        return make_issue('missing', {}, False, 'low')

    missing_summary = {
        col: {
            'missing_percentage': missing_per[col],
            'severity': (
                'low'
                if missing_per[col] <= MISSING_SEVERITY_THRESHOLD['low']
                else 'medium'
                if missing_per[col] <= MISSING_SEVERITY_THRESHOLD['medium']
                else 'high'
            ),
            'hint': 'Impute missing values if important, else drop',
        }
        for col in valid_missing
    }
 
    # `has_issue` is true if at least one column has non-zero missing.
    has_issue = any(float(v) > 0 for v in valid_missing.values())
    return make_issue('missing', missing_summary, has_issue, get_max_severity(missing_summary))
