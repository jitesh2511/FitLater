import pandas as pd
import numpy as np

from fitlater.profile.profiler import get_profile

def test_profile_structure():
    df = pd.DataFrame({
        'A': [1,2,3],
        'B': ['x','y','z']
    })

    result = get_profile(df)

    assert isinstance(result, dict)
    assert set(result.keys()) == {'A','B'}

def test_each_column_profile():
    df = pd.DataFrame({
        'A': [1,2,3],
        'B': [True, False, True]
    })

    result = get_profile(df)

    for col in df.columns:
        assert isinstance(result[col], dict)

def test_mixed_profile():
    df = pd.DataFrame({
        'num': [1,2,3,100],
        'cat': ['a','b','c','a'],
        'bool': [True, False, True, False],
        'missing': [1, None, np.nan, 4]
    })

    result = get_profile(df)

    assert result['num']['is_numeric'] is True
    assert result['cat']['is_numeric'] is False
    assert result['bool']['is_numeric'] is False
    assert result['missing']['missing_percentage'] > 0

def test_empty_df():
    df = pd.DataFrame()

    result = get_profile(df)

    assert result == {}

def test_profile_deterministic():
    df = pd.DataFrame({
        'A': [1,2,3]
    })

    r1 = get_profile(df)
    r2 = get_profile(df)

    assert r1 == r2