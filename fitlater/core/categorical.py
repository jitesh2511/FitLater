'''
This module contains functions to get statistics
for a categorical column in the dataset
'''

import pandas as pd

def get_categorical_stats(series:pd.Series) -> dict:

    n_unique = series.nunique()
    top_value = series.mode(dropna=True).iloc[0] if not series.empty else None
    top_value_freq = (series == top_value).sum()
    return {
        'n_unique': n_unique,
        'top_value': top_value,
        'top_freq' : top_value_freq
    }