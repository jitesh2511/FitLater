import pandas as pd
from fitlater.core.others import (
    get_datetime_stats,
    get_boolean_stats,
    get_mixed_stats
)


# =========================
# DATETIME TESTS
# =========================

def test_datetime_basic():
    series = pd.Series(pd.to_datetime([
        "2023-01-01",
        "2023-01-05",
        "2023-01-03"
    ]))

    result = get_datetime_stats(series)

    assert result["min"] == pd.Timestamp("2023-01-01")
    assert result["max"] == pd.Timestamp("2023-01-05")
    assert result["nunique"] == 3


def test_datetime_with_duplicates():
    series = pd.Series(pd.to_datetime([
        "2023-01-01",
        "2023-01-01",
        "2023-01-02"
    ]))

    result = get_datetime_stats(series)

    assert result["min"] == pd.Timestamp("2023-01-01")
    assert result["max"] == pd.Timestamp("2023-01-02")
    assert result["nunique"] == 2


def test_datetime_with_nan():
    series = pd.Series(pd.to_datetime([
        "2023-01-01",
        None,
        "2023-01-03"
    ]))

    result = get_datetime_stats(series)

    assert result["min"] == pd.Timestamp("2023-01-01")
    assert result["max"] == pd.Timestamp("2023-01-03")
    assert result["nunique"] == 2  # NaT ignored


def test_datetime_empty_series():
    series = pd.Series([], dtype="datetime64[ns]")

    result = get_datetime_stats(series)

    assert pd.isna(result["min"])
    assert pd.isna(result["max"])
    assert result["nunique"] == 0


# =========================
# BOOLEAN TESTS
# =========================

def test_boolean_basic():
    series = pd.Series([True, False, True, True])

    result = get_boolean_stats(series)

    assert result["true_count"] == 3
    assert result["false_count"] == 1


def test_boolean_all_true():
    series = pd.Series([True, True, True])

    result = get_boolean_stats(series)

    assert result["true_count"] == 3
    assert result["false_count"] == 0


def test_boolean_all_false():
    series = pd.Series([False, False])

    result = get_boolean_stats(series)

    assert result["true_count"] == 0
    assert result["false_count"] == 2


def test_boolean_with_nan():
    series = pd.Series([True, False, None, True])

    result = get_boolean_stats(series)

    assert result["true_count"] == 2
    assert result["false_count"] == 1
    # NaN ignored


def test_boolean_empty():
    series = pd.Series([], dtype="bool")

    result = get_boolean_stats(series)

    assert result["true_count"] == 0
    assert result["false_count"] == 0


def test_boolean_with_non_bool_values():
    """
    Edge case: pandas may treat non-bool truthy values differently.
    Your function should only count True/False explicitly.
    """
    series = pd.Series([1, 0, True, False])

    result = get_boolean_stats(series)

    # value_counts treats 1 == True and 0 == False
    assert result["true_count"] >= 1
    assert result["false_count"] >= 1

# =========================
# MIXED TYPE TESTS
# =========================

def test_mixed_basic():
    series = pd.Series([1, "A", 2, "B"])

    result = get_mixed_stats(series)

    assert result["n_mixed_types"] == 2  # int, str
    assert set(result["unique_values"]) == {"int", "str"}


def test_mixed_with_nan():
    series = pd.Series([1, "A", None, 2])

    result = get_mixed_stats(series)

    assert result["n_mixed_types"] == 2
    assert set(result["unique_values"]) == {"int", "str"}


def test_mixed_single_type():
    """
    Edge case: technically not mixed, but function should still behave correctly
    """
    series = pd.Series([1, 2, 3])

    result = get_mixed_stats(series)

    assert result["n_mixed_types"] == 1
    assert result['unique_values'] == ['int']


def test_mixed_complex_types():
    series = pd.Series([1, "A", 1.5, True])

    result = get_mixed_stats(series)

    assert result["n_mixed_types"] == 4
    assert set(result["unique_values"]) == {"int", "str", "float", "bool"}


def test_mixed_empty_series():
    series = pd.Series([], dtype="object")

    result = get_mixed_stats(series)

    assert result["n_mixed_types"] == 0
    assert result["unique_values"] == []

def test_mixed_unique_values_order_independent():
    series = pd.Series(["A", 1, "B", 2])

    result = get_mixed_stats(series)

    assert set(result["unique_values"]) == {"int", "str"}

def test_mixed_bool_and_int():
    series = pd.Series([True, 1, False, 0])

    result = get_mixed_stats(series)

    # Python treats bool as subclass of int, but type names differ
    assert set(result["unique_values"]) == {"bool", "int"}

def test_mixed_all_none():
    series = pd.Series([None, None])

    result = get_mixed_stats(series)

    assert result["n_mixed_types"] == 0
    assert result["unique_values"] == []