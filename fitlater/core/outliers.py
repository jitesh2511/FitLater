import pandas as pd
import numpy as np

def analyze_outliers(df:pd.DataFrame, outlier_threshold:float) -> dict:
    numeric = df.select_dtypes(include='number').columns

    if numeric.empty:
        return {
            'method':'IQR',
            'outlier_counts':None,
            'outlier_percentage':None,
            'columns_with_outlier':None,
            'bounds':None,
            'outlier_summary':None
        }
    
    quantiles = {col: {'Q1': np.quantile(df[col], q=0.25),
                       'Q3': np.quantile(df[col], q=0.75),
                       'IQR' : np.quantile(df[col], q=0.75) - np.quantile(df[col], q=0.25)}
                        for col in numeric}
    
    bounds = {col : {'lower_bound' : quantiles[col]['Q1'] - (quantiles[col]['IQR'] * 1.5),
                     'upper_bound' : quantiles[col]['Q3'] + (quantiles[col]['IQR'] * 1.5)}
                     for col in numeric}
    
    outlier_counts = {col : df[df[col]<bounds[col]['lower_bound']].value_counts().sum() + df[df[col]>bounds[col]['upper_bound']].value_counts().sum() 
                      for col in numeric}
    
    outlier_percentage = {col : round((outlier_counts[col] / len(df[col])) * 100, 2) for col in numeric}

    columns_with_outliers = [col for col in numeric if outlier_percentage[col]>(outlier_threshold*100)]

    outlier_summary = {
        'n_numeric_features' : len(numeric),
        'n_features_with_outliers' : len(columns_with_outliers),
        'max_outlier_percentage' : max(outlier_percentage.values())
    }

    return {
        'method' : 'IQR',
        'outlier_counts' : outlier_counts,
        'outlier_percentage' : outlier_percentage,
        'columns_with_outliers' : columns_with_outliers,
        'bounds' : bounds,
        'outlier_summary' : outlier_summary
    }