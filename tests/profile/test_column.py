from fitlater.profile.column import build_column_profile

import pandas as pd

def test_column_profile_structure():
    s = pd.Series([1,2,3])

    result = build_column_profile(s)

    assert set(result.keys()) == {
        'is_numeric',
        'missing_percentage',
        'outlier_percentage',
        'skew',
        'n_unique'
    }

def test_numeric_profile():
    s = pd.Series([1,2,3,4,5])

    result = build_column_profile(s)

    assert result['is_numeric'] is True
    assert result['skew'] is not None

def test_boolean_profile():
    s = pd.Series([True, False, True])

    result = build_column_profile(s)

    assert result['is_numeric'] is False
    assert result['outlier_percentage'] is None
    assert result['skew'] is None

def test_profile_missing():
    s = pd.Series([1, None, 3])

    result = build_column_profile(s)

    assert result['missing_percentage'] == 33.33

def test_n_unique():
    s = pd.Series([1,1,2,2,3])

    result = build_column_profile(s)

    assert result['n_unique'] == 3