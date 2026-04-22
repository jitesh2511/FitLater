import pytest
import pandas as pd
from fitlater.diagnostics.missing import check_missing


# =========================
# NORMAL CASES
# =========================

def test_no_missing_returns_none():
    series = pd.Series([1, 2, 3])
    profile = {"missing_count": 0, "missing_pct": 0.0}

    result = check_missing("col", profile, series)

    assert result is None


def test_missing_detected():
    series = pd.Series([1, None, 3])
    profile = {"missing_count": 1, "missing_pct": 33.33}

    result = check_missing("col", profile, series)

    assert result is not None
    assert result["type"] == "missing"
    assert result["column"] == "col"
    assert result["meta"]["has_issue"] is True

    assert result["data"]["issue_type"] == "missing_values"
    assert result["data"]["expected_type"] == "no_missing_values"
    assert result["data"]["current_type"] == "missing_values_present"


# =========================
# CONFIDENCE TESTS
# =========================

def test_confidence_calculation():
    series = pd.Series([1, None, None, 4])  # 50%
    profile = {"missing_count": 2, "missing_pct": 50.0}

    result = check_missing("col", profile, series)

    assert result["data"]["confidence"] == 0.5


def test_confidence_rounding():
    series = pd.Series([1, None, None])  # 66.67%
    profile = {"missing_count": 2, "missing_pct": 66.67}

    result = check_missing("col", profile, series)

    assert result["data"]["confidence"] == 0.67


# =========================
# SEVERITY TESTS
# =========================

def test_severity_low_medium_high():
    """
    This test depends on config thresholds but ensures
    severity is always valid
    """
    series = pd.Series([1, None])
    profile = {"missing_count": 1, "missing_pct": 50.0}

    result = check_missing("col", profile, series)

    assert result["meta"]["severity"] in ["low", "medium", "high"]


# =========================
# EDGE CASES
# =========================

def test_missing_profile_keys_missing():
    """
    If profile keys missing → defaults to 0 → no issue
    """
    series = pd.Series([1, None])
    profile = {}

    result = check_missing("col", profile, series)

    assert result is None


def test_missing_pct_zero_but_count_nonzero():
    """
    Inconsistent profile → function trusts profile
    """
    series = pd.Series([1, None])
    profile = {"missing_count": 1, "missing_pct": 0.0}

    result = check_missing("col", profile, series)

    assert result is not None
    assert result["data"]["confidence"] == 0.0


def test_missing_pct_100():
    series = pd.Series([None, None])
    profile = {"missing_count": 2, "missing_pct": 100.0}

    result = check_missing("col", profile, series)

    assert result["data"]["confidence"] == 1.0


def test_empty_series():
    series = pd.Series([], dtype="float")
    profile = {"missing_count": 0, "missing_pct": 0.0}

    result = check_missing("col", profile, series)

    assert result is None


# =========================
# DATA PAYLOAD VALIDATION
# =========================

def test_data_payload_structure():
    series = pd.Series([1, None])
    profile = {"missing_count": 1, "missing_pct": 50.0}

    result = check_missing("col", profile, series)

    data = result["data"]

    assert set(data.keys()) == {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert set(data["details"].keys()) == {
        "missing_count",
        "missing_pct"
    }


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_extra_keys_ignored():
    series = pd.Series([1, None])
    profile = {
        "missing_count": 1,
        "missing_pct": 50.0,
        "random_key": 123
    }

    result = check_missing("col", profile, series)

    assert result is not None


def test_series_not_used_for_logic():
    """
    Function depends ONLY on profile, not actual data
    """
    series = pd.Series([1, 2, 3])  # no missing
    profile = {"missing_count": 2, "missing_pct": 66.67}  # says missing

    result = check_missing("col", profile, series)

    assert result is not None