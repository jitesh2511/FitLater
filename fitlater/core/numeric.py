'''
This module contains functions to calculate the 
numerical statistics of a numerical column
'''

import pandas as pd

def get_numeric_stats(series:pd.Series) -> dict:

    numerical_summary = series.agg(
        ['mean','median','std','min','max','skew','kurt']
    ).to_dict()

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    numerical_summary['q1'] = q1
    numerical_summary['q3'] = q3

    return numerical_summary