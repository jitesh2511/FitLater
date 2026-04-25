import pytest
import pandas as pd
from fitlater.diagnostics.duplicates import check_duplicates


# =========================
# NORMAL CASES
# =========================

def test_no_duplicates_returns_none():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6]
    })

    result = check_duplicates({}, df)

    assert result is None


def test_duplicates_detected():
    df = pd.DataFrame({
        "A": [1, 1, 2],
        "B": [3, 3, 4]
    })

    result = check_duplicates({}, df)

    assert result is not None
    assert result["type"] == "duplicates"
    assert result["column"] == "dataset"
    assert result["meta"]["has_issue"] is True

    assert result["data"]["issue_type"] == "duplicate_rows"
    assert result["data"]["current_type"] == "duplicate_present"


# =========================
# CONFIDENCE TESTS
# =========================

def test_confidence_calculation():
    df = pd.DataFrame({
        "A": [1, 1, 2, 3],
        "B": [4, 4, 5, 6]
    })
    # 1 duplicate row out of 4 → 0.25

    result = check_duplicates({}, df)

    assert result["data"]["confidence"] == 0.25


def test_confidence_rounding():
    df = pd.DataFrame({
        "A": [1, 1, 1, 2, 3],
        "B": [4, 4, 4, 5, 6]
    })
    # 2 duplicates out of 5 → 0.4

    result = check_duplicates({}, df)

    assert result["data"]["confidence"] == 0.4


# =========================
# EDGE CASES
# =========================

def test_empty_dataframe():
    df = pd.DataFrame()

    result = check_duplicates({}, df)

    assert result is None


def test_all_rows_same():
    """
    Extreme case: all duplicates except first row
    """
    df = pd.DataFrame({
        "A": [1, 1, 1, 1],
        "B": [2, 2, 2, 2]
    })

    result = check_duplicates({}, df)

    assert result is not None
    assert result["data"]["confidence"] == 0.75  # 3/4


def test_single_row():
    df = pd.DataFrame({"A": [1]})

    result = check_duplicates({}, df)

    assert result is None


# =========================
# BOUNDARY CONDITIONS
# =========================

def test_duplicate_percentage_calculation():
    df = pd.DataFrame({
        "A": [1, 1, 2, 2],
        "B": [3, 3, 4, 4]
    })
    # 2 duplicates out of 4 → 50%

    result = check_duplicates({}, df)

    assert result["data"]["details"]["duplicate_pct"] == 50.0


def test_severity_value_valid():
    df = pd.DataFrame({
        "A": [1, 1, 2],
        "B": [3, 3, 4]
    })

    result = check_duplicates({}, df)

    assert result["meta"]["severity"] in ["low", "medium", "high"]


# =========================
# STRUCTURE VALIDATION
# =========================

def test_data_payload_structure():
    df = pd.DataFrame({
        "A": [1, 1, 2],
        "B": [3, 3, 4]
    })

    result = check_duplicates({}, df)

    data = result["data"]

    assert set(data.keys()) == {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert set(data["details"].keys()) == {
        "duplicate_count",
        "duplicate_pct"
    }


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    """
    Profile is not used → ensure no dependency
    """
    df = pd.DataFrame({
        "A": [1, 1, 2],
        "B": [3, 3, 4]
    })

    profile = {"random": 123}

    result = check_duplicates(profile, df)

    assert result is not None


def test_mixed_dtype_duplicates():
    """
    Duplicate detection should work across types
    """
    df = pd.DataFrame({
        "A": [1, 1, "1"],
        "B": [2, 2, "2"]
    })

    result = check_duplicates({}, df)

    # Only first two rows are duplicates
    assert result is not None