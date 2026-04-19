import pandas as pd
import numpy as np

from fitlater.profile.stats import is_numeric
from fitlater.profile.stats import get_outlier_percentage
from fitlater.profile.stats import get_missing_percentage



def test_is_numeric():
    df = pd.DataFrame({
        'int': [1,2,3],
        'float': [1.0,2.0,3.0],
        'bool': [True, False, True],
        'str': ['a','b','c']
    })

    assert is_numeric(df['int']) is True
    assert is_numeric(df['float']) is True
    assert is_numeric(df['bool']) is True  # pandas behavior
    assert is_numeric(df['str']) is False

def test_missing_percentage():
    s = pd.Series([1, None, np.nan, 4])

    result = get_missing_percentage(s)

    assert result == 50.0

def test_no_missing():
    s = pd.Series([1,2,3])

    assert get_missing_percentage(s) == 0.0

def test_outlier_percentage_basic():
    s = pd.Series([10]*95 + [100, 120, 150, 200, 300])

    result = get_outlier_percentage(s)

    assert result > 0

def test_outlier_boolean():
    s = pd.Series([True, False, True, False])

    result = get_outlier_percentage(s)

    assert result is None

def test_outlier_non_numeric():
    s = pd.Series(['a','b','c'])

    result = get_outlier_percentage(s)

    assert result is None

def test_outlier_all_nan():
    s = pd.Series([np.nan]*10)

    result = get_outlier_percentage(s)

    # could be 0 or None depending on your design
    assert result == 0.0 or result is None