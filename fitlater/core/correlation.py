import pandas as pd
import numpy as np

def analyze_correlation(df:pd.DataFrame, corr_threshold) -> dict:

    numerical = df.select_dtypes(include='number').columns

    # Remove numeric columns that are completely empty (all NaN)
    nonempty_numerical = [col for col in numerical if not df[col].isnull().all()]
    numerical = pd.Index(nonempty_numerical)

    if numerical.empty:
        return {
            'corr_matrix': None,
            'high_corr_pairs': [],
            'corr_summary': None,
        }
    
    # Correlation Matrix
    corr = df[numerical].corr()

    upper_tri = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

    # High Correlation Pairs
    high_corr = upper_tri[abs(upper_tri) > corr_threshold].stack()
    high_corr_list = [{'feature_1': idx[0], 'feature_2': idx[1], 'correlation': round(value,4)} for idx, value in high_corr.items()]

    # Correlation Summary
    corr_sum = {
        'n_numeric_features':len(numerical),
        'n_high_corr_pairs':len(high_corr_list),
        'max_corr': round(upper_tri.stack().max(), 4),
        'mean_abs_corr': round(upper_tri.abs().stack().mean(), 4)
    }

    return {
        'corr_matrix': corr,
        'high_corr_pairs': high_corr_list,
        'corr_summary': corr_sum
    }