from fitlater.diagnostics.base import make_issue
from fitlater.diagnostics.base import get_max_severity
from fitlater.config import SKEW_SEVERITY_THRESHOLD
from fitlater.config import SKEW_THRESHOLD
import pandas as pd

def check_distribution(data:pd.DataFrame) -> dict:

    numeric_features = data.select_dtypes(include='number').columns.to_list()

    # Exclude columns with >=60% missing values
    numeric_features = [col for col in numeric_features if data[col].isna().mean() < 0.6]

    if not numeric_features:
        return make_issue('distribution', None, False, 'low')

    high_skew = [col for col in numeric_features if abs(data[col].skew()) > SKEW_THRESHOLD]

    if not high_skew:
        return make_issue('distribution', None, False, 'low')

    skew_values = {col : data[col].skew() for col in high_skew}

    skew_summary = {col : {
        'skew' : round(skew_values[col], 4),
        'severity' : 'low' if abs(skew_values[col]) <= SKEW_SEVERITY_THRESHOLD['low'] 
        else 'medium' if abs(skew_values[col]) <= SKEW_SEVERITY_THRESHOLD['medium']
        else 'high',
        'hint' : 'Apply approporiate transformation'
    } for col in high_skew}


    return make_issue('distribution', skew_summary, True, get_max_severity(skew_summary))

    