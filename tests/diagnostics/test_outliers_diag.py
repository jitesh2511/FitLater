from fitlater.diagnostics.outliers import check_outliers
from fitlater.core.outliers import analyze_outliers
from fitlater.config import OUTLIER_THRESHOLD

import pandas as pd
import numpy as np
import pytest

def create_outlier_df():
    np.random.seed(42)
    n = 50

    # 1. Normal distribution, a few injected extreme outliers
    feature_norm = np.random.normal(loc=10, scale=2, size=n)
    feature_norm[5] = 30   # clear high outlier
    feature_norm[6] = -8   # clear low outlier

    # 2. Symmetric, all values same: no IQR, not flagged
    feature_constant = np.full(n, 15.0)

    # 3. Categorical feature: should never be flagged
    feature_cat = ['cat'] * 25 + ['dog'] * 20 + ['owl'] * 5

    # 4. Boolean feature: should never be flagged
    feature_bool = [True, False] * (n // 2) + [True] * (n % 2)

    # 5. Unique values: e.g., index-like, not flagged (as outliers are all singletons, IQR not meaningful)
    feature_unique = np.arange(100, 100 + n)

    # 6. All NaN feature: should not be flagged at all
    feature_nan = [np.nan] * n

    # 7. Many NaN, but enough valid for IQR
    feature_some_nan = np.random.normal(0, 1, size=n)
    feature_some_nan[:10] = np.nan
    feature_some_nan[11] = 10  # outlier in valid region

    # 8. Nearly all missing, just two or three values (should not be flagged, too few to compute IQR)
    feature_too_few = [np.nan] * (n-2) + [0, 100]

    # 9. Mix of zeros and very high/low outliers
    feature_bimodal = np.zeros(n)
    feature_bimodal[:3] = [99, -99, 50]  # 3 large outliers

    df = pd.DataFrame({
        "feature_norm": feature_norm,
        "feature_constant": feature_constant,
        "feature_cat": feature_cat,
        "feature_bool": feature_bool,
        "feature_unique": feature_unique,
        "feature_nan": feature_nan,
        "feature_some_nan": feature_some_nan,
        "feature_too_few": feature_too_few,
        "feature_bimodal": feature_bimodal
    })
    return check_outliers(analyze_outliers(df, OUTLIER_THRESHOLD))

def test_outlier_structure():
    outliers = create_outlier_df()
    assert isinstance(outliers, dict)
    assert isinstance(outliers['meta'], dict)
    expected_keys = {'type', 'data', 'meta'}
    meta_keys = {'has_issue', 'max_severity'}
    assert set(outliers.keys()) == expected_keys
    assert set(outliers['meta'].keys()) == meta_keys

def test_outlier_values():
    outliers = create_outlier_df()

    # type/meta keys
    assert outliers['type'] == 'outliers'
    assert isinstance(outliers['meta'], dict)
    assert 'has_issue' in outliers['meta']
    assert 'max_severity' in outliers['meta']
    assert isinstance(outliers['data'], dict)

    outlier_keys = set(outliers['data'].keys())

    # Columns that MUST NOT be in result (categorical, boolean, all nan, only a couple non-nan)
    forbidden_cols = {'feature_cat', 'feature_bool', 'feature_nan', 'feature_too_few'}
    for col in forbidden_cols:
        assert col not in outlier_keys

    # Columns that MUST be present and have outliers: normal with injected, bimodal with injected, some_nan (enough data)
    must_have = {'feature_norm', 'feature_bimodal', 'feature_some_nan'}
    for col in must_have:
        assert col in outlier_keys

    # feature_norm: should see 2/50 = 4% outliers, sometimes more if IQR is tight.
    norm_stats = outliers['data']['feature_norm']
    assert isinstance(norm_stats, dict)
    # Allow 4%±2% to allow for slightly variable IQR calculation
    assert abs(norm_stats['outlier_percentage'] - 4.0) < 2.1
    assert norm_stats['severity'] in ('low', 'medium', 'high')

    # feature_bimodal: 6% outliers (3/50 = 6.0%), sometimes more/less if IQR is tight
    bimodal_stats = outliers['data']['feature_bimodal']
    assert isinstance(bimodal_stats, dict)
    assert abs(bimodal_stats['outlier_percentage'] - 6.0) < 2.1

    # feature_some_nan: 1 clear outlier out of 40 valid = 2.5%
    some_nan_stats = outliers['data']['feature_some_nan']
    assert isinstance(some_nan_stats, dict)
    assert some_nan_stats['outlier_percentage'] >= 2.0

    # feature_constant: Should be in outliers, but outlier_percentage = 0
    if 'feature_constant' in outlier_keys:
        constant_stats = outliers['data']['feature_constant']
        assert constant_stats['outlier_percentage'] == 0.0

    # feature_unique: may or may not be present depending on logic, but if present, should be zero outlier percentage
    if 'feature_unique' in outlier_keys:
        unique_stats = outliers['data']['feature_unique']
        assert unique_stats['outlier_percentage'] == 0.0

@pytest.mark.parametrize("bad_input", [None, 123, "string", [], {}])
def test_invalid_input(bad_input):
    with pytest.raises(Exception):
        check_outliers(analyze_outliers(bad_input))

def test_empty_dataframe():
    df = pd.DataFrame()
    result = check_outliers(analyze_outliers(df, OUTLIER_THRESHOLD))

    assert result['meta']['has_issue'] is False

def test_no_outliers_case():
    df = pd.DataFrame({
        'A': np.linspace(1, 100, 100)
    })

    result = check_outliers(analyze_outliers(df, OUTLIER_THRESHOLD))

    assert not result['meta']['has_issue']