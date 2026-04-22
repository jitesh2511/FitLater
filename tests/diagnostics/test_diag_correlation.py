import pytest
import pandas as pd
from fitlater.diagnostics.correlation import check_correlation_all


# =========================
# NORMAL CASES
# =========================

def test_no_numeric_columns():
    df = pd.DataFrame({
        "A": ["x", "y"],
        "B": ["a", "b"]
    })
    profiles = {
        "A": {"type": "categorical"},
        "B": {"type": "categorical"}
    }

    result = check_correlation_all(profiles, df)

    assert result == []


def test_single_numeric_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    profiles = {"A": {"type": "numeric"}}

    result = check_correlation_all(profiles, df)

    assert result == []


def test_low_correlation():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [4, 1, 3, 2]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    assert result == []


def test_high_correlation_detected():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [2, 4, 6, 8]  # perfectly correlated
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    assert len(result) == 1

    issue = result[0]

    assert issue["type"] == "corr"
    assert issue["meta"]["has_issue"] is True
    assert issue["data"]["issue_type"] == "high_correlation"


# =========================
# CONFIDENCE TESTS
# =========================

def test_confidence_value():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [2, 4, 6, 8]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    assert result[0]["data"]["confidence"] == 1.0


def test_negative_correlation():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [8, 6, 4, 2]  # perfectly negative
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    assert len(result) == 1
    assert result[0]["data"]["confidence"] == 1.0


# =========================
# EDGE CASES
# =========================

def test_constant_column():
    """
    Correlation becomes NaN → should be ignored
    """
    df = pd.DataFrame({
        "A": [1, 1, 1, 1],
        "B": [2, 4, 6, 8]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    assert result == []


def test_nan_values():
    df = pd.DataFrame({
        "A": [1, 2, None, 4],
        "B": [2, 4, 6, 8]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    # Should still compute correlation ignoring NaN
    assert isinstance(result, list)


def test_empty_dataframe():
    df = pd.DataFrame()
    profiles = {}

    result = check_correlation_all(profiles, df)

    assert result == []


# =========================
# MULTI-COLUMN TESTS
# =========================

def test_multiple_numeric_columns():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [2, 4, 6, 8],
        "C": [5, 3, 6, 1]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"},
        "C": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    # Only A-B should be strongly correlated
    assert len(result) == 1


def test_no_duplicate_pairs():
    """
    Ensure (A,B) and (B,A) are not duplicated
    """
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [2, 4, 6, 8]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    assert len(result) == 1


# =========================
# STRUCTURE VALIDATION
# =========================

def test_data_payload_structure():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [2, 4, 6, 8]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = check_correlation_all(profiles, df)

    issue = result[0]
    data = issue["data"]

    assert set(data.keys()) == {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert "correlation" in data["details"]


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_mismatch_with_data():
    """
    Profiles say numeric but data is not
    """
    df = pd.DataFrame({
        "A": ["x", "y", "z"],
        "B": ["a", "b", "c"]
    })
    profiles = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    # corr() will fail → should raise
    with pytest.raises(Exception):
        check_correlation_all(profiles, df)