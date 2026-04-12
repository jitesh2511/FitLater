import pandas as pd
import numpy as np

def analyze_outliers(df:pd.DataFrame, outlier_threshold:float) -> dict:
    numeric = df.select_dtypes(include='number').columns

    skipped_columns = {}

    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            skipped_columns[col] = 'non_numeric'
            continue

        missing_ratio = df[col].isna().mean()

        if missing_ratio > 0.6:
            skipped_columns[col] = 'too_many_missing'
            continue
    # Exclude numeric columns with more than 60% missing values
    numeric = [col for col in numeric if df[col].isna().mean() <= 0.6]

    if not numeric:
        return {
            'method': 'IQR',
            'outlier_counts': {},
            'outlier_percentage': {},
            'columns_with_outliers': [],
            'bounds': {},
            'skipped_columns': skipped_columns,
            'outlier_summary': {
                'n_numeric_features': 0,
                'n_features_with_outliers': 0,
                'max_outlier_percentage': 0
            }
        }
    
    quantiles = {
        col: {
            'Q1': np.nanquantile(df[col], q=0.25),
            'Q3': np.nanquantile(df[col], q=0.75),
            'IQR': np.nanquantile(df[col], q=0.75) - np.nanquantile(df[col], q=0.25)
        }
        for col in numeric
    }
    
    bounds = {
        col: {
            'lower_bound': quantiles[col]['Q1'] - (quantiles[col]['IQR'] * 1.5),
            'upper_bound': quantiles[col]['Q3'] + (quantiles[col]['IQR'] * 1.5)
        }
        for col in numeric
    }
    
    outlier_counts = {
        col: int(
            ((df[col] < bounds[col]['lower_bound']) | (df[col] > bounds[col]['upper_bound'])).sum(skipna=True)
        )
        for col in numeric
    }
    
    outlier_percentage = {
        col: round((outlier_counts[col] / df[col].count()) * 100, 2) if df[col].count() > 0 else 0.0
        for col in numeric
    }

    columns_with_outliers = [col for col in numeric if outlier_percentage[col] > (outlier_threshold * 100)]

    outlier_summary = {
        'n_numeric_features': len(numeric),
        'n_features_with_outliers': len(columns_with_outliers),
        'max_outlier_percentage': max(outlier_percentage.values()) if outlier_percentage else None
    }

    return {
        'method': 'IQR',
        'outlier_counts': outlier_counts,
        'outlier_percentage': outlier_percentage,
        'columns_with_outliers': columns_with_outliers,
        'bounds': bounds,
        'skipped_columns': skipped_columns,
        'outlier_summary': outlier_summary
    }