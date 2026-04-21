'''
This module defines functions to get statistics
of dtypes other than numeric or categorical
'''

import pandas as pd

# Get statistics for DateTime dtype
def get_datetime_stats(series:pd.Series) -> dict:

    return series.agg(['min','max','nunique']).to_dict()

# Get statitics for Boolean dtype
def get_boolean_stats(series:pd.Series) -> dict:

    value_counts = series.value_counts()

    return {
        'true_count': value_counts.get(True, 0),
        'false_count': value_counts.get(False, 0)
    }

# Get statistics for Mixed type
def get_mixed_stats(series:pd.Series) -> dict:

    n_mixed_types = series.dropna().map(type).nunique()

    return {
        'n_mixed_types': n_mixed_types
    }