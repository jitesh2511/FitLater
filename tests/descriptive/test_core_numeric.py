import pytest
import pandas as pd
from fitlater.core.numeric import get_numeric_stats


def test_basic_numeric_stats():
    series = pd.Series([1, 2, 3, 4, 5])

    result = get_numeric_stats(series)

    assert result["mean"] == 3
    assert result["median"] == 3
    assert result["min"] == 1
    assert result["max"] == 5

    assert result["q1"] == 2
    assert result["q3"] == 4


def test_with_floats():
    series = pd.Series([1.5, 2.5, 3.5])

    result = get_numeric_stats(series)

    assert result["mean"] == pytest.approx(2.5)
    assert result["median"] == pytest.approx(2.5)
    assert result["min"] == 1.5
    assert result["max"] == 3.5


def test_with_negative_values():
    series = pd.Series([-5, -1, 0, 1, 5])

    result = get_numeric_stats(series)

    assert result["min"] == -5
    assert result["max"] == 5
    assert result["median"] == 0


def test_with_nan_values():
    series = pd.Series([1, 2, None, 4, 5])

    result = get_numeric_stats(series)

    # pandas ignores NaN by default
    assert result["mean"] == pytest.approx(3)
    assert result["median"] == 3
    assert result["min"] == 1
    assert result["max"] == 5


def test_all_nan_series():
    series = pd.Series([None, None, None], dtype="float")

    result = get_numeric_stats(series)

    # All should be NaN
    for key in ["mean", "median", "std", "min", "max", "skew", "kurt", "q1", "q3"]:
        assert pd.isna(result[key])


def test_single_value_series():
    series = pd.Series([10])

    result = get_numeric_stats(series)

    assert result["mean"] == 10
    assert result["median"] == 10
    assert result["min"] == 10
    assert result["max"] == 10

    # std, skew, kurt may be NaN for single value
    assert pd.isna(result["std"])
    assert pd.isna(result["skew"])
    assert pd.isna(result["kurt"])


def test_constant_series():
    series = pd.Series([5, 5, 5, 5])

    result = get_numeric_stats(series)

    assert result["mean"] == 5
    assert result["median"] == 5
    assert result["min"] == 5
    assert result["max"] == 5

    # std = 0, skew/kurt may be NaN
    assert result["std"] == 0


def test_output_keys():
    series = pd.Series([1, 2, 3])

    result = get_numeric_stats(series)

    expected_keys = {
        "mean", "median", "std", "min", "max", "skew", "kurt",
        "q1", "q3"
    }

    assert set(result.keys()) == expected_keys


def test_large_numbers():
    series = pd.Series([1e10, 1e11, 1e12])

    result = get_numeric_stats(series)

    assert result["max"] == 1e12
    assert result["min"] == 1e10