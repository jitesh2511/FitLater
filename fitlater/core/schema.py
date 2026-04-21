'''
This module is used to check the dtype of all the columns in the dataset
'''

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_bool_dtype, is_datetime64_any_dtype

from fitlater.config import IDENTIFIER_THRESHOLD, NUMERIC_LIKE_RATIO_THRESHOLD

def infer_column_types(df:pd.DataFrame) -> dict:

    return {
        col: infer_single_column(df[col]) for col in df.columns
    }

def infer_single_column(series):

    '''
    dtypes checked for :-
    - Empty (empty column)
    - Numeric
    - Boolean
    - DateTime
    - Identifier
    - Categorical
    - Mixed 
    '''

    if len(series.dropna()) == 0:
        return 'empty'

    # Direct types
    if is_bool_dtype(series):
        return 'boolean'

    if is_numeric_dtype(series):
        return 'numeric'
    
    if is_datetime64_any_dtype(series):
        return 'datetime'

    non_null = series.dropna()
    is_mixed = non_null.map(type).nunique() > 1
    if is_mixed:
        return 'mixed'

    n_unique = series.nunique(dropna=True)
    n_total = len(series)

    # Checking for a numeric like string
    numeric_coercion = pd.to_numeric(non_null, errors='coerce')
    numeric_ratio = numeric_coercion.notna().sum() / len(non_null) if len(non_null) > 0 else 0

    is_numeric_like = numeric_ratio > NUMERIC_LIKE_RATIO_THRESHOLD

    if not is_numeric_like:
        if n_total > 0 and (n_unique / n_total) > IDENTIFIER_THRESHOLD:
            return 'identifier'
    
    return 'categorical'