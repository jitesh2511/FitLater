import pandas as pd
from fitlater.core.schema import (
    infer_column_types,
    infer_single_column
)


# =========================
# SINGLE COLUMN TESTS
# =========================

def test_empty_column():
    series = pd.Series([None, None])

    assert infer_single_column(series) == "empty"


def test_boolean_column():
    series = pd.Series([True, False, True])

    assert infer_single_column(series) == "boolean"


def test_numeric_column():
    series = pd.Series([1, 2, 3])

    assert infer_single_column(series) == "numeric"


def test_datetime_column():
    series = pd.Series(pd.to_datetime(["2023-01-01", "2023-01-02"]))

    assert infer_single_column(series) == "datetime"


def test_identifier_column():
    """
    High uniqueness ratio → identifier
    """
    series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8])

    result = infer_single_column(series)

    assert result in ["identifier", "numeric"]
    # depends on IDENTIFIER_THRESHOLD


def test_categorical_low_unique():
    series = pd.Series(["A", "B", "A", "C"])

    assert infer_single_column(series) == "categorical"


def test_categorical_high_unique_below_threshold():
    series = pd.Series([f"user_{i}" for i in range(10)])

    result = infer_single_column(series)

    assert result in ["identifier", "categorical"]


def test_numeric_stored_as_string():
    """
    IMPORTANT: should remain categorical (no coercion)
    """
    series = pd.Series(["1", "2", "3"])

    assert infer_single_column(series) == "categorical"

def test_with_nan_values():
    series = pd.Series(["A", "B", None, "A"])

    assert infer_single_column(series) == "categorical"


# =========================
# FULL DATAFRAME TESTS
# =========================

def test_infer_column_types_basic():
    df = pd.DataFrame({
        "num": [1, 2, 3],
        "cat": ["A", "B", "A"],
        "bool": [True, False, True]
    })

    result = infer_column_types(df)

    assert result["num"] == "numeric"
    assert result["cat"] == "categorical"
    assert result["bool"] == "boolean"


def test_infer_column_types_empty_column():
    df = pd.DataFrame({
        "empty": [None, None],
        "num": [1, 2]
    })

    result = infer_column_types(df)

    assert result["empty"] == "empty"
    assert result["num"] == "numeric"


def test_infer_column_types_datetime():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02"])
    })

    result = infer_column_types(df)

    assert result["date"] == "datetime"


def test_infer_column_types_identifier_case():
    df = pd.DataFrame({
        "id": list(range(100))  # high uniqueness
    })

    result = infer_column_types(df)

    assert result["id"] in ["identifier", "numeric"]


def test_output_structure():
    df = pd.DataFrame({
        "A": [1],
        "B": ["x"]
    })

    result = infer_column_types(df)

    assert isinstance(result, dict)
    assert set(result.keys()) == {"A", "B"}

# =========================
# MIXED TYPE TESTS
# =========================

def test_infer_mixed_basic():
    series = pd.Series([1, "A", 2, "B"])

    assert infer_single_column(series) == "mixed"


def test_infer_mixed_with_nan():
    series = pd.Series([1, "A", None, 2])

    assert infer_single_column(series) == "mixed"
    

def test_infer_numeric_like_string_not_mixed():
    """
    Should NOT be mixed, should go through numeric-like logic
    """
    series = pd.Series(["1", "2", "3"])

    assert infer_single_column(series) == "categorical"


def test_infer_mixed_priority_over_identifier():
    """
    Mixed should override identifier logic even if uniqueness is high
    """
    series = pd.Series([1, "A", 2, "B"])

    result = infer_single_column(series)

    assert result == "mixed"


def test_infer_dataframe_with_mixed_column():
    df = pd.DataFrame({
        "mixed_col": [1, "A", 2],
        "num_col": [1, 2, 3]
    })

    result = infer_column_types(df)

    assert result["mixed_col"] == "mixed"
    assert result["num_col"] == "numeric"