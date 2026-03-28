from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import SKEW_SEVERITY_THRESHOLD
from fitlater.config import SKEW_THRESHOLD
import pandas as pd

def check_distribution(data:pd.DataFrame) -> dict:

    numeric_features = data.select_dtypes(include='number').columns.to_list()

    if numeric_features.empty:
        return make_issue('distribution', None, False, 'low')

    high_skew = [col for col in numeric_features if data[col].skew() > SKEW_THRESHOLD]

    if skew.empty:
        return make_issue('distribution', None, False, 'low')

    skew_values = {col : data[col].skew() for col in high_skew}

    skew_summary = {col : {
        'skew' : skew_values[col],
        'severity' : 'low' if skew_values[col] <= SKEW_SEVERITY_THRESHOLD['low'] 
        else 'medium' if skew_values[col] <= SKEW_SEVERITY_THRESHOLD['medium']
        else 'high',
        'hint' : 'Apply approporiate transformation'
    } for col in high_skew}


    return make_issue('distribution', skew_summary, True, get_max_severity(skew_summary))

    