from fitlater.diagnostics.correlation import check_correlation
from fitlater.core.correlation import analyze_correlation
from fitlater.config import CORRELATION_THRESHOLD

import pandas as pd
import numpy as np

def create_corr_edge_df():
    """
    Returns a dataframe testing edge cases for correlation diagnostics:
        - All numeric, some strongly correlated, some not at all
        - One constant column (zero variance)
        - All identical rows except one (affecting correlation calculations)
        - Some columns entirely NaN or almost NaN
        - Mixture of int and float types
        - Includes a column with just two unique values
        - No numeric columns scenario (for completeness)
    """
    np.random.seed(42)
    n = 10

    data = {
        # Two highly correlated columns (perfect, and one noisy)
        "perfect_corr1": np.arange(n),
        "perfect_corr2": np.arange(n),
        "noisy_corr": np.arange(n) + np.random.normal(0, 0.1, size=n),

        # Some moderately correlated, manually constructed
        "half_corr": np.linspace(0, 10, n) + np.linspace(10, 0, n),

        # One completely random column
        "random_col": np.random.rand(n),

        # Constant column, zero variance
        "constant": np.ones(n),

        # Column with one outlier row
        "one_outlier": np.ones(n),
        # Will change the last value to be an outlier
        # Column with NaNs
        "mostly_nan": [np.nan]*8 + [1, 2],

        # Mixture of int/float
        "int_col": np.arange(n),
        "float_col": np.arange(n).astype(float) / 3.0,

        # Two unique values only (could be interpreted as bool)
        "binary_col": [0, 0, 1, 1, 0, 1, 0, 1, 0, 1],

        # All NaN column
        "all_nan": [np.nan] * n
    }

    df = pd.DataFrame(data)
    # Add outlier
    df.loc[n-1, "one_outlier"] = 10

    # Add a non-numeric column for negative test
    df['cat_col'] = ['A']*5 + ['B']*5

    return check_correlation(analyze_correlation(df, CORRELATION_THRESHOLD))

def test_corr_structure():

    corr = create_corr_edge_df()

    # Test the structure of the returned dictionary
    assert isinstance(corr, dict)
    assert set(corr.keys()) == {'type', 'data', 'meta'}
    
    assert isinstance(corr['meta'], dict)
    assert set(corr['meta'].keys()) == {'has_issue', 'max_severity'}
    
def test_corr_values():

    corr = create_corr_edge_df()

    assert corr['type'] == 'correlation'
    assert corr['meta']['max_severity'] in ['low', 'medium', 'high']

    data = corr['data']

    if data: 

        assert corr['meta']['has_issue'] is True

        # Check every pair's structure and key content
        for k, v in data.items():
            assert isinstance(v, dict)
            assert {'feature_1', 'feature_2', 'correlation', 'severity', 'hint'} == set(v.keys())
            assert v['severity'] in ['low', 'medium', 'high']
            assert isinstance(v['correlation'], float) or isinstance(v['correlation'], int)
            assert isinstance(v['feature_1'], str)
            assert isinstance(v['feature_2'], str)

        # Sanity check: no pairs where all feature names are the same
        for v in data.values():
            assert v['feature_1'] != v['feature_2']

        # Check that no pair involves a non-numeric or all-NaN column
        for v in data.values():
            assert v['feature_1'] not in ['cat_col', 'all_nan']
            assert v['feature_2'] not in ['cat_col', 'all_nan']

        # Check that a perfect corr pair is picked up as high severity, e.g. 1.0 or very close
        found_perfect = False
        for v in data.values():
            # This line checks if the current pair of features consists of 'perfect_corr1' and 'perfect_corr2' (regardless of order)
            # AND that their correlation value is essentially perfect (i.e., exactly 1 within a tiny numerical margin).
            if (set([v['feature_1'], v['feature_2']]) == {'perfect_corr1', 'perfect_corr2'}) and abs(v['correlation'] - 1.0) < 1e-8:
                assert v['severity'] == 'high'
                found_perfect = True
        assert found_perfect

    else:
        # If data is None or {}, means no high correlation pairs, max_severity should be 'low'
        assert corr['data'] is None or corr['data'] == {}
        assert corr['meta']['max_severity'] == 'low'
        assert not corr['meta']['has_issue']
