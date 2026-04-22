import pytest
import pandas as pd
from fitlater.diagnostics.constant_column import check_constant


# =========================
# NORMAL CASES
# =========================

def test_constant_column_detected():
    series = pd.Series([5, 5, 5])
    profile = {"n_unique": 1, "type": "numeric"}

    result = check_constant("col", profile, series)

    assert result is not None
    assert result["type"] == "constant"
    assert result["column"] == "col"
    assert result["meta"]["severity"] == "high"
    assert result["meta"]["has_issue"] is True

    assert result["data"]["issue_type"] == "constant_column"
    assert result["data"]["expected_type"] == "variable"
    assert result["data"]["current_type"] == "numeric"
    assert result["data"]["confidence"] == 1.0


def test_non_constant_column_returns_none():
    series = pd.Series([1, 2, 3])
    profile = {"n_unique": 3, "type": "numeric"}

    result = check_constant("col", profile, series)

    assert result is None


# =========================
# EDGE CASES
# =========================

def test_missing_n_unique_in_profile():
    """
    If n_unique is missing, defaults to 0 → should NOT trigger constant
    """
    series = pd.Series([5, 5, 5])
    profile = {"type": "numeric"}

    result = check_constant("col", profile, series)

    assert result is None


def test_empty_series():
    """
    Empty column should not be treated as constant
    """
    series = pd.Series([], dtype="float")
    profile = {"n_unique": 0, "type": "numeric"}

    result = check_constant("col", profile, series)

    assert result is None


def test_all_nan_series():
    """
    All NaN → n_unique usually 0 → should not be constant
    """
    series = pd.Series([None, None])
    profile = {"n_unique": 0, "type": "numeric"}

    result = check_constant("col", profile, series)

    assert result is None


def test_constant_string_column():
    series = pd.Series(["A", "A", "A"])
    profile = {"n_unique": 1, "type": "categorical"}

    result = check_constant("col", profile, series)

    assert result is not None
    assert result["data"]["current_type"] == "categorical"


# =========================
# BEHAVIOR VALIDATION
# =========================

def test_data_payload_structure():
    series = pd.Series([1, 1])
    profile = {"n_unique": 1, "type": "numeric"}

    result = check_constant("col", profile, series)

    data = result["data"]

    expected_keys = {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert set(data.keys()) == expected_keys


def test_confidence_is_one():
    """
    Constant detection should always be certain
    """
    series = pd.Series([10, 10])
    profile = {"n_unique": 1, "type": "numeric"}

    result = check_constant("col", profile, series)

    assert result["data"]["confidence"] == 1.0


# =========================
# STABILITY / ROBUSTNESS
# =========================

def test_profile_extra_keys_do_not_affect():
    series = pd.Series([5, 5, 5])
    profile = {
        "n_unique": 1,
        "type": "numeric",
        "random_key": 123
    }

    result = check_constant("col", profile, series)

    assert result is not None


def test_series_not_used_for_logic():
    """
    Even if series is inconsistent, decision depends ONLY on profile
    """
    series = pd.Series([1, 2, 3])  # not constant
    profile = {"n_unique": 1, "type": "numeric"}  # says constant

    result = check_constant("col", profile, series)

    # Function trusts profile → should still flag
    assert result is not None