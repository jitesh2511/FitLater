import pandas as pd
from fitlater.profile.stats import is_numeric, get_missing_percentage, get_outlier_percentage

def build_column_profile(series: pd.Series):

    numeric = is_numeric(series) and not pd.api.types.is_bool_dtype(series)
    skew = series.skew() if numeric else None

    return {
        'is_numeric': numeric,
        'missing_percentage': get_missing_percentage(series),
        'outlier_percentage': get_outlier_percentage(series),
        'skew': None if pd.isna(skew) else skew,
        'n_unique': series.nunique()
    }