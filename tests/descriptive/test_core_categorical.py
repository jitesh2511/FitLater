import pandas as pd
from fitlater.core.categorical import get_categorical_stats


def test_basic_categorical_stats():
    series = pd.Series(["A", "B", "A", "C", "A"])

    result = get_categorical_stats(series)

    assert result["n_unique"] == 3
    assert result["top_value"] == "A"
    assert result["top_freq"] == 3


def test_single_value_series():
    series = pd.Series(["A", "A", "A"])

    result = get_categorical_stats(series)

    assert result["n_unique"] == 1
    assert result["top_value"] == "A"
    assert result["top_freq"] == 3


def test_all_unique_values():
    series = pd.Series(["A", "B", "C", "D"])

    result = get_categorical_stats(series)

    assert result["n_unique"] == 4
    # mode returns first in sorted order usually
    assert result["top_value"] in ["A", "B", "C", "D"]
    assert result["top_freq"] == 1


def test_empty_series():
    series = pd.Series([], dtype="object")

    result = get_categorical_stats(series)

    assert result["n_unique"] == 0
    assert result["top_value"] is None
    assert result["top_freq"] == 0


def test_series_with_nan():
    series = pd.Series(["A", "B", None, "A", None])

    result = get_categorical_stats(series)

    assert result["n_unique"] == 2  # NaN excluded by nunique()
    assert result["top_value"] == "A"
    assert result["top_freq"] == 2


def test_multiple_modes():
    series = pd.Series(["A", "B", "A", "B"])

    result = get_categorical_stats(series)

    # pandas returns multiple modes
    assert result["top_value"] in ["A", "B"]
    assert result["top_freq"] == 2


def test_numeric_categorical():
    """
    Even if numbers are passed, function should still work
    since pandas treats them as categorical-like here.
    """
    series = pd.Series([1, 2, 1, 3, 1])

    result = get_categorical_stats(series)

    assert result["n_unique"] == 3
    assert result["top_value"] == 1
    assert result["top_freq"] == 3


def test_mixed_types():
    series = pd.Series(["A", 1, "A", 1, 1])

    result = get_categorical_stats(series)

    assert result["n_unique"] == 2
    assert result["top_value"] == 1
    assert result["top_freq"] == 3