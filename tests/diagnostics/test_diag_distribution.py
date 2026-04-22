import pytest
import pandas as pd
from fitlater.diagnostics.distribution import check_distribution


# =========================
# NORMAL CASES
# =========================

def test_no_issue_when_not_numeric():
    series = pd.Series(["A", "B", "C"])
    profile = {"type": "categorical", "skew": 2.0}

    result = check_distribution("col", profile, series)

    assert result is None


def test_no_issue_when_skew_below_threshold():
    series = pd.Series([1, 2, 3])
    profile = {"type": "numeric", "skew": 0.5}

    result = check_distribution("col", profile, series)

    assert result is None


def test_high_skew_detected():
    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": 2.5,
        "kurt": 3.0
    }

    result = check_distribution("col", profile, series)

    assert result is not None
    assert result["type"] == "distribution"
    assert result["column"] == "col"
    assert result["meta"]["has_issue"] is True

    assert result["data"]["issue_type"] == "skewed_column"
    assert result["data"]["current_type"] == "high_skew"


# =========================
# CONFIDENCE TESTS
# =========================

def test_confidence_uses_absolute_skew():
    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": -2.34,
        "kurt": 3.0
    }

    result = check_distribution("col", profile, series)

    assert result["data"]["confidence"] == 2.34


def test_confidence_rounding():
    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": 2.3456,
        "kurt": 3.1234
    }

    result = check_distribution("col", profile, series)

    assert result["data"]["confidence"] == 2.35


# =========================
# EDGE CASES
# =========================

def test_skew_none_returns_none():
    series = pd.Series([1, 2, 3])
    profile = {"type": "numeric", "skew": None}

    result = check_distribution("col", profile, series)

    assert result is None


def test_missing_kurt_in_profile():
    """
    kurt missing → profile.get('kurt') returns None → round(None) will fail
    """
    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": 2.5
    }

    with pytest.raises(TypeError):
        check_distribution("col", profile, series)


def test_empty_series():
    series = pd.Series([], dtype="float")
    profile = {"type": "numeric", "skew": 0.0}

    result = check_distribution("col", profile, series)

    assert result is None


# =========================
# BOUNDARY CONDITIONS
# =========================

def test_skew_exact_threshold():
    """
    If skew == threshold → should NOT trigger (strict > condition)
    """
    from fitlater.config import SKEW_THRESHOLD

    series = pd.Series([1, 2, 3])
    profile = {
        "type": "numeric",
        "skew": SKEW_THRESHOLD,
        "kurt": 0.0
    }

    result = check_distribution("col", profile, series)

    assert result is None


def test_skew_just_above_threshold():
    from fitlater.config import SKEW_THRESHOLD

    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": SKEW_THRESHOLD + 0.01,
        "kurt": 1.0
    }

    result = check_distribution("col", profile, series)

    assert result is not None


# =========================
# DATA PAYLOAD VALIDATION
# =========================

def test_data_payload_structure():
    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": 2.0,
        "kurt": 3.0
    }

    result = check_distribution("col", profile, series)

    data = result["data"]

    assert set(data.keys()) == {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert set(data["details"].keys()) == {
        "skew",
        "kurt"
    }


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_extra_keys_ignored():
    series = pd.Series([1, 2, 3, 100])
    profile = {
        "type": "numeric",
        "skew": 2.0,
        "kurt": 3.0,
        "random": 123
    }

    result = check_distribution("col", profile, series)

    assert result is not None


def test_series_not_used_for_logic():
    """
    Function depends ONLY on profile skew, not actual data
    """
    series = pd.Series([1, 2, 3])  # not skewed
    profile = {
        "type": "numeric",
        "skew": 3.0,
        "kurt": 1.0
    }

    result = check_distribution("col", profile, series)

    assert result is not None