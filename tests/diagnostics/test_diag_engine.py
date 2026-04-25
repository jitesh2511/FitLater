import pytest
import pandas as pd
from fitlater.diagnostics.engine import build_diagnostics


# =========================
# BASIC STRUCTURE
# =========================

def test_empty_dataframe():
    df = pd.DataFrame()
    profile = {}

    result = build_diagnostics(profile, df)

    assert result == []


def test_no_issues():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
    })

    profile = {
        "A": {"type": "numeric", "missing_count": 0, "missing_pct": 0.0, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0},
        "B": {"type": "categorical", "missing_count": 0, "missing_pct": 0.0, "top_freq": 1, "n_unique": 3}
    }

    result = build_diagnostics(profile, df)

    assert isinstance(result, list)
    assert result == []


# =========================
# COLUMN-LEVEL ISSUES
# =========================

def test_missing_issue_detected():
    df = pd.DataFrame({"A": [1, None, 3]})
    profile = {
        "A": {"type": "numeric", "missing_count": 1, "missing_pct": 33.33, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0}
    }

    result = build_diagnostics(profile, df)

    assert any(issue["type"] == "missing" for issue in result)


def test_multiple_column_issues():
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": ["1", "2", "3"]
    })

    profile = {
        "A": {"type": "numeric", "missing_count": 1, "missing_pct": 33.33, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0},
        "B": {"type": "categorical", "missing_count": 0, "missing_pct": 0.0}
    }

    result = build_diagnostics(profile, df)

    assert len(result) >= 1


# =========================
# DATASET-LEVEL ISSUES
# =========================

def test_duplicates_detected():
    df = pd.DataFrame({
        "A": [1, 1, 2],
        "B": [3, 3, 4]
    })

    profile = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = build_diagnostics(profile, df)

    assert any(issue["type"] == "duplicates" for issue in result)


def test_correlation_detected():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [2, 4, 6, 8]
    })

    profile = {
        "A": {"type": "numeric"},
        "B": {"type": "numeric"}
    }

    result = build_diagnostics(profile, df)

    assert any(issue["type"] == "corr" for issue in result)


# =========================
# MIXED SCENARIOS
# =========================

def test_combined_issues():
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": [2, 4, 6],
        "C": [2, 4, 6],  # correlated with B
        "D": ["1", "2", "3"]
    })

    profile = {
        "A": {"type": "numeric", "missing_count": 1, "missing_pct": 33.33, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0},
        "B": {"type": "numeric", "q1": 2, "q3": 6, "skew": 0.0, "kurt": 0.0},
        "C": {"type": "numeric", "q1": 2, "q3": 6, "skew": 0.0, "kurt": 0.0},
        "D": {"type": "categorical", "missing_count": 0, "missing_pct": 0.0}
    }

    result = build_diagnostics(profile, df)

    types = [issue["type"] for issue in result]

    assert "missing" in types
    assert "corr" in types
    assert "type_issue" in types


# =========================
# ORDER / DUPLICATION SAFETY
# =========================

def test_no_duplicate_issues():
    """
    Ensure same issue not repeated multiple times unnecessarily
    """
    df = pd.DataFrame({
        "A": [1, None, 3]
    })

    profile = {
        "A": {"type": "numeric", "missing_count": 1, "missing_pct": 33.33, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0}
    }

    result = build_diagnostics(profile, df)

    issue_types = [issue["type"] for issue in result]

    assert issue_types.count("missing") == 1


# =========================
# ROBUSTNESS TESTS
# =========================


def test_profile_extra_columns_ignored():
    df = pd.DataFrame({"A": [1, 2, 3]})
    profile = {
        "A": {"type": "numeric", "missing_count": 0, "missing_pct": 0.0, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0},
        "B": {"type": "numeric"}
    }

    result = build_diagnostics(profile, df)

    assert isinstance(result, list)


# =========================
# OUTPUT STRUCTURE
# =========================

def test_all_issues_have_consistent_structure():
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": [2, 4, 6]
    })

    profile = {
        "A": {"type": "numeric", "missing_count": 1, "missing_pct": 33.33, "q1": 1, "q3": 3, "skew": 0.0, "kurt": 0.0},
        "B": {"type": "numeric", "q1": 2, "q3": 6, "skew": 0.0, "kurt": 0.0}
    }

    result = build_diagnostics(profile, df)

    for issue in result:
        assert "type" in issue
        assert "data" in issue
        assert "meta" in issue