import pytest
from fitlater.advisory.duplicates import handle_duplicates


# =========================
# NORMAL CASES
# =========================

def test_high_severity_duplicates():
    diag = {
        "data": {"details": {"duplicate_pct": 40}},
        "meta": {"severity": "high"}
    }

    result = handle_duplicates({}, diag)

    assert result["column"] == "dataset"
    assert result["issue_type"] == "duplicates"
    assert result["action"] == "Remove duplicate rows immediately"
    assert "40%" in result["reason"]
    assert result["priority"] == 1


def test_medium_severity_duplicates():
    diag = {
        "data": {"details": {"duplicate_pct": 15}},
        "meta": {"severity": "medium"}
    }

    result = handle_duplicates({}, diag)

    assert result["action"] == "Consider removing duplicate rows"
    assert "15%" in result["reason"]
    assert result["priority"] == 2


# =========================
# LOW 
# =========================

def test_low_severity_returns_low_priority():
    diag = {
        "data": {"details": {"duplicate_pct": 5}},
        "meta": {"severity": "low"}
    }

    result = handle_duplicates({}, diag)

    assert result is not None
    assert result["priority"] == 3
    assert result["action"] == "No immediate action required"


def test_missing_severity_returns_low_priority():
    diag = {
        "data": {"details": {"duplicate_pct": 20}},
        "meta": {}
    }

    result = handle_duplicates({}, diag)

    assert result is not None
    assert result["priority"] == 3


# =========================
# EDGE CASES
# =========================

def test_zero_duplicates_high_severity():
    """
    Inconsistent input: 0% but severity high
    Advisory trusts diagnostics
    """
    diag = {
        "data": {"details": {"duplicate_pct": 0}},
        "meta": {"severity": "high"}
    }

    result = handle_duplicates({}, diag)

    assert result is not None
    assert "0%" in result["reason"]


def test_extreme_duplicates_100_percent():
    diag = {
        "data": {"details": {"duplicate_pct": 100}},
        "meta": {"severity": "high"}
    }

    result = handle_duplicates({}, diag)

    assert "100%" in result["reason"]


# =========================
# FAILURE CASES
# =========================

def test_missing_data_key():
    diag = {
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_duplicates({}, diag)


def test_missing_details_key():
    diag = {
        "data": {},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_duplicates({}, diag)


def test_missing_duplicate_pct():
    diag = {
        "data": {"details": {}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_duplicates({}, diag)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    profile = {"random": 123}
    diag = {
        "data": {"details": {"duplicate_pct": 20}},
        "meta": {"severity": "high"}
    }

    result = handle_duplicates(profile, diag)

    assert result["column"] == "dataset"


def test_extra_diag_keys_ignored():
    diag = {
        "data": {"details": {"duplicate_pct": 20}},
        "meta": {"severity": "high"},
        "noise": "random"
    }

    result = handle_duplicates({}, diag)

    assert result["column"] == "dataset"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "data": {"details": {"duplicate_pct": 20}},
        "meta": {"severity": "high"}
    }

    r1 = handle_duplicates({}, diag)
    r2 = handle_duplicates({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_invalid_severity_value_returns_low_priority():
    diag = {
        "data": {"details": {"duplicate_pct": 20}},
        "meta": {"severity": "critical"}
    }

    result = handle_duplicates({}, diag)

    assert result is not None
    assert result["priority"] == 3


def test_non_numeric_duplicate_pct():
    diag = {
        "data": {"details": {"duplicate_pct": "invalid"}},
        "meta": {"severity": "high"}
    }

    result = handle_duplicates({}, diag)

    # No crash, but weird output
    assert "invalid%" in result["reason"]