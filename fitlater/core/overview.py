import pandas as pd

def analyze(data: pd.DataFrame) -> dict:
    
    if (data.empty):
        return {
            'shape': {
                'n_rows': data.shape[0],
                'n_cols': data.shape[1]
            },
            'column_classification': {
                'numerical': [],
                'categorical': [],
                'boolean': [],
                'others': []
            },
            'categorical_summary': {},
            'missing': {
                'total_missing': 0,
                'missing_per_column': {},
                'missing_percentage': {}
            },
            'numerical_summary': {},
            'duplicates': {
                'n_dup': 0
            }
        }
    
    columns = data.columns

    # Shape
    n_rows = data.shape[0]
    n_cols = data.shape[1]
    memory = data.memory_usage(deep=True).sum() / (1024 ** 2)
    shape = {
        'n_rows':n_rows,
        'n_cols':n_cols,
        'memory_usage': round(memory,4)
    }


    # Column Classification
    numerical = data.select_dtypes(include='number').columns.tolist()
    boolean = data.select_dtypes(include='bool').columns.tolist()
    categorical = [
        col
        for col in data.columns
        if pd.api.types.is_object_dtype(data[col].dtype)
        or isinstance(data[col].dtype, pd.CategoricalDtype)
        or pd.api.types.is_string_dtype(data[col].dtype)
    ]
    classified = set(numerical) | set(boolean) | set(categorical)
    others = [col for col in data.columns if col not in classified]
    column_classification = {
        'numerical':numerical,
        'boolean':boolean,
        'categorical':categorical,
        'others':others
    }
    
    # Missing
    total_missing = data.isnull().sum().sum()
    col_missing = data.isnull().sum().to_dict()
    missing_percentage = {col: (p/n_rows) * 100 for col, p in col_missing.items()}
    missing = {
        'total_missing':total_missing,
        'missing_per_column':col_missing,
        'missing_percentage':missing_percentage
    }

    # Numerical Summary
    numerical_summary = data[numerical].agg(['mean','median','std','min','max','skew']).to_dict()
    
    # Categorical Summary
    categorical_summary = {}

    for col in categorical:

        series = data[col]
        n_unique = series.nunique()

        if series.dropna().empty:
            top_value = None
            top_freq = 0
        else:
            mode_series = series.mode(dropna=True)
            top_value = mode_series.iloc[0] if not mode_series.empty else None
            top_freq = series.value_counts(dropna=True).iloc[0] if not series.value_counts(dropna=True).empty else 0

        categorical_summary[col] = {
            'n_unique':n_unique,
            'top_value':top_value,
            'top_freq':top_freq
        }

    # Duplicates
    n_duplicates = data.duplicated().sum()
    duplicate_per = (n_duplicates/n_rows) * 100
    duplicates = {
        'n_dup':n_duplicates,
        'dup_per':duplicate_per
    }

    result = {
        'shape':shape,
        'column_classification':column_classification,
        'categorical_summary': categorical_summary,
        'missing':missing,
        'numerical_summary':numerical_summary,
        'duplicates':duplicates
    }
    
    return result