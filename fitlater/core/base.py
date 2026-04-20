'''
This module contains helper functions
'''

import pandas as pd

def get_metadata(df:pd.DataFrame) -> dict:

    rows = df.shape[0]
    cols = df.shape[1]

    memory_bytes = df.memory_usage(deep=True).sum()
    if memory_bytes < 1024:
        memory_str = f"{memory_bytes} B"
    elif memory_bytes < 1024 ** 2:
        memory_str = f"{memory_bytes / 1024:.2f} KB"
    else:
        memory_str = f"{memory_bytes / (1024 ** 2):.2f} MB"

    return {
        "rows": rows,
        "cols": cols,
        "memory": memory_str
    }

def get_missing(series:pd.Series) -> dict:

    count = series.isna().sum()
    prct = round(series.isna().mean() * 100, 2)

    return{
        'missing_count': count,
        'missing_pct': prct
    }