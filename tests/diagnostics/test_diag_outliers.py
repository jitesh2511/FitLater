import pytest
import pandas as pd
from fitlater.diagnostics.outliers import check_outliers


# =========================
# NORMAL CASES
# =========================

def test_no_outliers_returns_none():
    series = pd.Series([10, 12, 14, 16, 18])
    profile = {
        "type": "numeric",
        "q1": 12,
        "q3": 16
    }

    result = check_outliers("col", profile, series)

    assert result is None


def test_outliers_detected():
    series = pd.Series([10, 12, 14, 16, 100])  # 100 is outlier
    profile = {
        "type": "numeric",
        "q1": 12,
        "q3": 16
    }

    result = check_outliers("col", profile, series)

    assert result is not None
    assert result["type"] == "outliers"
    assert result["column"] == "col"
    assert result["meta"]["has_issue"] is True

    assert result["data"]["issue_type"] == "outlier_values"
    assert result["data"]["current_type"] == "outliers_present"


# =========================
# CONFIDENCE TESTS
# =========================

def test_confidence_calculation():
    series = pd.Series([10, 12, 14, 16, 100])  # 1 out of 5
    profile = {
        "type": "numeric",
        "q1": 12,
        "q3": 16
    }

    result = check_outliers("col", profile, series)

    # 1/5 = 20% → 0.2
    assert result["data"]["confidence"] == 0.2


def test_confidence_rounding():
    series = pd.Series([1, 2, 3, 100, 200])  # 2 outliers out of 5 → 40%
    profile = {
        "type": "numeric",
        "q1": 2,
        "q3": 3
    }

    result = check_outliers("col", profile, series)

    assert result["data"]["confidence"] == 0.4


# =========================
# EDGE CASES
# =========================

def test_non_numeric_column():
    series = pd.Series(["A", "B", "C"])
    profile = {
        "type": "categorical",
        "q1": None,
        "q3": None
    }

    result = check_outliers("col", profile, series)

    assert result is None


def test_empty_series():
    series = pd.Series([], dtype="float")
    profile = {
        "type": "numeric",
        "q1": 0,
        "q3": 0
    }

    result = check_outliers("col", profile, series)

    assert result is None


def test_all_nan_series():
    series = pd.Series([None, None])
    profile = {
        "type": "numeric",
        "q1": 0,
        "q3": 0
    }

    result = check_outliers("col", profile, series)

    assert result is None


def test_zero_iqr():
    """
    All values same → IQR = 0 → no outliers
    """
    series = pd.Series([5, 5, 5, 5])
    profile = {
        "type": "numeric",
        "q1": 5,
        "q3": 5
    }

    result = check_outliers("col", profile, series)

    assert result is None


# =========================
# BOUNDARY CONDITIONS
# =========================

def test_boundary_values_not_outliers():
    """
    Values exactly on bounds should NOT be outliers
    """
    series = pd.Series([10, 12, 14, 16, 18])
    profile = {
        "type": "numeric",
        "q1": 12,
        "q3": 16
    }

    # lb = 12 - 1.5*4 = 6
    # ub = 16 + 1.5*4 = 22
    # all values within range

    result = check_outliers("col", profile, series)

    assert result is None


# =========================
# DATA PAYLOAD VALIDATION
# =========================

def test_data_payload_structure():
    series = pd.Series([10, 12, 14, 16, 100])
    profile = {
        "type": "numeric",
        "q1": 12,
        "q3": 16
    }

    result = check_outliers("col", profile, series)

    data = result["data"]

    assert set(data.keys()) == {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert set(data["details"].keys()) == {
        "outlier_count",
        "outlier_pct"
    }


# =========================
# ROBUSTNESS TESTS
# =========================


def test_series_not_used_for_type():
    """
    Function trusts profile type, not actual data
    """
    series = pd.Series(["A", "B", "C"])
    profile = {
        "type": "numeric",  # incorrect
        "q1": 1,
        "q3": 2
    }

    # Will attempt numeric comparison → should fail
    with pytest.raises(TypeError):
        check_outliers("col", profile, series)