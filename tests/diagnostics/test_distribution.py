from fitlater.diagnostics.distribution import check_distribution

import pandas as pd
import numpy as np

import pytest

def create_distribution_edge_df():
    np.random.seed(42)
    n = 60

    # 1. Normal distribution, mean ~0, very low skew
    feature_norm = np.random.normal(0, 1, n)
    
    # 2. Strong positive skew (exponential)
    feature_pos_skew = np.random.exponential(1, n)  # Skew > 1

    # 3. Strong negative skew (reverse exponential)
    feature_neg_skew = -np.random.exponential(1, n)  # Skew < -1

    # 4. All zeros (constant), should not be flagged as skewed
    feature_zeros = np.zeros(n)
    
    # 5. Mixed ints/floats, mild skew
    feature_mild_skew = np.concatenate([
        np.random.normal(10, 2, n//2),
        np.random.normal(11, 2, n//2)
    ])

    # 6. All missing (NaN) values
    feature_nan = [np.nan]*n

    # 7. More than 80% missing, rest tightly skewed (should be ignored by implementation if threshold for missing is <0.6)
    feature_mostly_nan = [np.nan]*int(0.85*n) + [10, 11, 12, 50, 100, 500, -200, -300, -999]

    # 8. All unique values (linear spaced), skew zero
    feature_unique = np.linspace(-5, 5, n)

    # 9. Categorical, non-numeric (should be ignored)
    feature_cat = ['A']*15 + ['B']*15 + ['C']*15 + ['D']*15

    # 10. Boolean column (should be ignored)
    feature_bool = [True, False] * (n//2) + [True]*(n % 2)

    df = pd.DataFrame({
        "feature_norm": feature_norm,
        "feature_pos_skew": feature_pos_skew,
        "feature_neg_skew": feature_neg_skew,
        "feature_zeros": feature_zeros,
        "feature_mild_skew": feature_mild_skew,
        "feature_nan": feature_nan,
        "feature_mostly_nan": feature_mostly_nan,
        "feature_unique": feature_unique,
        "feature_cat": feature_cat,
        "feature_bool": feature_bool
    })
    return df

def test_distribution_structure():
    df = create_distribution_edge_df()
    result = check_distribution(df)

    # Type/Meta keys
    assert isinstance(result, dict)
    assert {'type', 'data', 'meta'} == set(result.keys())
    assert result['type'] == 'distribution'
    assert isinstance(result['meta'], dict)
    assert 'has_issue' in result['meta'] and 'max_severity' in result['meta']

def test_distribution_values():
    df = create_distribution_edge_df()
    result = check_distribution(df)

    data = result['data']

    # Categorical and boolean columns MUST NOT be present in data keys
    forbidden = {'feature_cat', 'feature_bool', 'feature_nan', 'feature_mostly_nan'}
    if data:
        for c in forbidden:
            assert c not in data, f"Non-numeric or all-nan field '{c}' shouldn't be present"

        # Strongly skewed columns must appear if above SKEW_THRESHOLD (typically 1.0 in config)
        assert 'feature_pos_skew' in data.keys()
        assert 'feature_neg_skew' in data.keys()

        # Skew values should match orientation
        pos_skew_stats = data['feature_pos_skew']
        assert pos_skew_stats['skew'] > 1
        assert pos_skew_stats['severity'] in ('low', 'medium', 'high')
        assert isinstance(pos_skew_stats['hint'], str)

        neg_skew_stats = data['feature_neg_skew']
        assert neg_skew_stats['skew'] < -1
        assert neg_skew_stats['severity'] in ('low', 'medium', 'high')

        # Columns with nearly-zero or zero skew (normal, all-zeros, all-unique, mild skew) must not be present
        for col in ('feature_norm', 'feature_zeros', 'feature_unique'):
            assert col not in data, f"{col} should NOT be flagged as skewed"

    else:
        # If no issues, data should be None
        assert not result['meta']['has_issue']
        assert result['meta']['max_severity'] == 'low'


@pytest.mark.parametrize("bad_input", [None, 123, "string", [], {}])
def test_invalid_input(bad_input):
    with pytest.raises(Exception):
        check_distribution(bad_input)
    
def test_empty_dataframe():
    df = pd.DataFrame()
    result = check_distribution(df)

    assert result['meta']['has_issue'] is False

def test_no_skew_case():
    df = pd.DataFrame({
        'A': np.random.normal(0, 1, 100)
    })

    result = check_distribution(df)

    assert not result['meta']['has_issue']