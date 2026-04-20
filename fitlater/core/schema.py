'''
This module is used to check the dtype of all the columns in the dataset
'''

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_bool_dtype, is_datetime64_any_dtype

from fitlater.config import IDENTIFIER_THRESHOLD

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

    n_unique = series.nunique(dropna=True)
    n_total = len(series)

    if n_total > 0 and (n_unique / n_total) > IDENTIFIER_THRESHOLD:
        return 'identifier'
    
    if n_unique < 20:
        return 'categorical'
    
    return 'categorical'