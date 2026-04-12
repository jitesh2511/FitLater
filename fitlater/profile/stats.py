import pandas as pd
import numpy as np

def is_numeric(series: pd.Series) -> bool:
    
    res = pd.api.types.is_numeric_dtype(series)
    return res

def get_missing_percentage(series: pd.Series):
    
    missing = series.isnull().sum()
    
    return round((missing/series.shape[0]) * 100, 2)

def get_outlier_percentage(series: pd.Series):

    # Skip non-numeric or boolean
    if not is_numeric(series) or pd.api.types.is_bool_dtype(series):
        return None

    # handle all-NaN or insufficient data
    valid = series.dropna()
    if valid.shape[0] == 0:
        return None

    Q3 = np.nanquantile(valid, q=0.75)
    Q1 = np.nanquantile(valid, q=0.25)
    IQR = Q3 - Q1

    lb = Q1 - (1.5 * IQR)
    ub = Q3 + (1.5 * IQR)

    outliers = int(((valid < lb) | (valid > ub)).sum())

    return round((outliers / series.shape[0]) * 100, 2)