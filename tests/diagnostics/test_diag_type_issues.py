import pandas as pd
import numpy as np

from fitlater.diagnostics.type_issues import check_type_issues, check_numeric_conversion


# =========================
# NORMAL CASES
# =========================

def test_non_categorical_returns_none():
    series = pd.Series([1, 2, 3])
    profile = {"type": "numeric"}

    result = check_type_issues("col", profile, series)

    assert result is None


def test_empty_series_returns_none():
    series = pd.Series([None, None])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is None


# =========================
# NUMERIC AS STRING
# =========================

def test_numeric_as_string_detected():
    series = pd.Series(["1", "2", "3", "4"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None
    assert result["data"]["issue_type"] == "numeric_as_string"
    assert result["data"]["expected_type"] == "numeric"
    assert result["meta"]["severity"] == "high"


def test_numeric_as_string_confidence():
    series = pd.Series(["1", "2", "x", "4"])  # 3/4 = 0.75
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result["data"]["confidence"] == 0.75


# =========================
# DATETIME AS STRING
# =========================

def test_datetime_as_string_detected():
    series = pd.Series(["2023-01-01", "2023-02-01", "2023-03-01"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None
    assert result["data"]["issue_type"] == "datetime_as_string"
    assert result["data"]["expected_type"] == "datetime"


def test_datetime_confidence():
    series = pd.Series(["2023-01-01", "not_date", "2024-04-11", "2023-12-25", "2023-06-17", "2023-09-23", "2025-07-21", "2025-01-01", "2024-05-15", "2024-06-26", "2025-02-28"])  # 10/11
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result["data"]["confidence"] == round(10/11, 2)


# =========================
# BOOLEAN AS STRING
# =========================

def test_boolean_as_string_detected():
    series = pd.Series(["true", "false", "true"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None
    assert result["data"]["issue_type"] == "boolean_as_string"
    assert result["meta"]["severity"] == "medium"


def test_boolean_case_insensitive():
    series = pd.Series(["True", " FALSE ", "true"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None
    assert set(result["data"]["details"]["values"]) == {"true", "false"}


# =========================
# MIXED NUMERIC
# =========================

def test_mixed_numeric_detected():
    series = pd.Series(["1", "2", "x", "y"])  # partial numeric
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None
    assert result["data"]["issue_type"] == "mixed_types"
    assert result["meta"]["severity"] == "medium"


# =========================
# PRIORITY TESTS (VERY IMPORTANT)
# =========================

def test_numeric_priority_over_datetime():
    """
    If both numeric and datetime possible → numeric should win
    (because it's checked first)
    """
    series = pd.Series(["1", "2", "3"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result["data"]["issue_type"] == "numeric_as_string"


def test_datetime_priority_over_boolean():
    """
    Datetime check comes before boolean
    """
    series = pd.Series(["2023-01-01", "2023-01-02"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result["data"]["issue_type"] == "datetime_as_string"


# =========================
# EDGE CASES
# =========================

def test_single_unique_value_not_boolean():
    """
    Boolean requires >1 unique values
    """
    series = pd.Series(["true", "true"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    # Should NOT trigger boolean
    assert result is None or result["data"]["issue_type"] != "boolean_as_string"


def test_whitespace_handling():
    series = pd.Series([" 1 ", "2", " 3"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None


def test_nan_ignored():
    series = pd.Series(["1", None, "2", None])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is not None


# =========================
# NO ISSUE CASES
# =========================

def test_clean_categorical_returns_none():
    series = pd.Series(["A", "B", "C"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is None


def test_random_strings_returns_none():
    series = pd.Series(["apple", "banana", "car"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    assert result is None


# =========================
# DATA STRUCTURE VALIDATION
# =========================

def test_data_payload_structure():
    series = pd.Series(["1", "2", "3"])
    profile = {"type": "categorical"}

    result = check_type_issues("col", profile, series)

    data = result["data"]

    assert "expected_type" in data
    assert "current_type" in data
    assert "issue_type" in data
    assert "confidence" in data
    assert "details" in data


# =========================
# ROBUSTNESS TESTS
# =========================

def test_series_not_used_for_type_decision():
    """
    Profile decides if logic runs
    """
    series = pd.Series(["1", "2", "3"])
    profile = {"type": "numeric"}  # wrong

    result = check_type_issues("col", profile, series)

    assert result is None


# Added new tests for check_numeric_conversion()


# -----------------------------
# POSITIVE CASES (should detect)
# -----------------------------

def test_detect_boolean_01():
    s = pd.Series([0, 1, 0, 1, 1])
    result = check_numeric_conversion("col", s)

    assert result is not None
    assert result["data"]["issue_type"] == "boolean_as_numeric"
    assert result["data"]["expected_type"] == "boolean"
    assert result["data"]["current_type"] == "numeric"
    assert result["meta"]["severity"] == "medium"


def test_detect_boolean_with_nan():
    s = pd.Series([0, 1, np.nan, 1, 0])
    result = check_numeric_conversion("col", s)

    assert result is not None


def test_detect_boolean_float_values():
    s = pd.Series([0.0, 1.0, 1.0, 0.0])
    result = check_numeric_conversion("col", s)

    assert result is not None


# -----------------------------
# NEGATIVE CASES (should NOT detect)
# -----------------------------

def test_non_boolean_numeric():
    s = pd.Series([0, 1, 2, 3])
    result = check_numeric_conversion("col", s)

    assert result is None


def test_single_value_only():
    s = pd.Series([1, 1, 1, 1])
    result = check_numeric_conversion("col", s)

    # Should not classify single constant column as boolean encoding
    assert result is None


def test_string_values():
    s = pd.Series(["0", "1", "0"])
    result = check_numeric_conversion("col", s)

    assert result is None


def test_mixed_numeric():
    s = pd.Series([0, 1, 2, 1])
    result = check_numeric_conversion("col", s)

    assert result is None


# -----------------------------
# EDGE CASES (important)
# -----------------------------

def test_empty_series():
    s = pd.Series([])
    result = check_numeric_conversion("col", s)

    assert result is None


def test_all_nan_series():
    s = pd.Series([np.nan, np.nan])
    result = check_numeric_conversion("col", s)

    assert result is None


def test_boolean_dtype_series():
    s = pd.Series([True, False, True])
    result = check_numeric_conversion("col", s)

    # Already boolean → should not flag
    assert result is None


def test_negative_values():
    s = pd.Series([-1, 0, 1])
    result = check_numeric_conversion("col", s)

    assert result is None


def test_large_series_boolean_pattern():
    s = pd.Series([0, 1] * 5000)
    result = check_numeric_conversion("col", s)

    assert result is not None


# -----------------------------
# CONTRACT TESTS (important)
# -----------------------------

def test_output_structure():
    s = pd.Series([0, 1])
    result = check_numeric_conversion("col", s)

    assert "type" in result
    assert "column" in result
    assert "data" in result
    assert "meta" in result

    assert result["meta"]["has_issue"] is True
    assert result["meta"]["severity"] == "medium"