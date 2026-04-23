import pytest
from fitlater.advisory.outliers import handle_outliers


# =========================
# NORMAL CASES
# =========================

def test_high_severity_outliers():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 35}},
        "meta": {"severity": "high"}
    }

    result = handle_outliers({}, diag)

    assert result["column"] == "A"
    assert result["issue_type"] == "outliers"
    assert result["action"] == "Investigate data or consider dropping column"
    assert "35%" in result["reason"]
    assert result["priority"] == 1


def test_medium_severity_outliers():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 12}},
        "meta": {"severity": "medium"}
    }

    result = handle_outliers({}, diag)

    assert result["action"] == "Apply capping or transformation"
    assert "12%" in result["reason"]
    assert result["priority"] == 2


# =========================
# LOW / NO ADVICE
# =========================

def test_low_severity_returns_none():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 5}},
        "meta": {"severity": "low"}
    }

    result = handle_outliers({}, diag)

    assert result is None


def test_missing_severity_returns_none():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 20}},
        "meta": {}
    }

    result = handle_outliers({}, diag)

    assert result is None


# =========================
# EDGE CASES
# =========================

def test_zero_outliers_high_severity():
    """
    Inconsistent input: 0% but severity high
    Advisory trusts diagnostics
    """
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 0}},
        "meta": {"severity": "high"}
    }

    result = handle_outliers({}, diag)

    assert result is not None
    assert "0%" in result["reason"]


def test_extreme_outliers_100_percent():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 100}},
        "meta": {"severity": "high"}
    }

    result = handle_outliers({}, diag)

    assert "100%" in result["reason"]


# =========================
# FAILURE CASES
# =========================

def test_missing_data_key():
    diag = {
        "column": "A",
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_outliers({}, diag)


def test_missing_details_key():
    diag = {
        "column": "A",
        "data": {},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_outliers({}, diag)


def test_missing_outlier_pct():
    diag = {
        "column": "A",
        "data": {"details": {}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_outliers({}, diag)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    profile = {"random": 123}
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 20}},
        "meta": {"severity": "high"}
    }

    result = handle_outliers(profile, diag)

    assert result["column"] == "A"


def test_extra_diag_keys_ignored():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 20}},
        "meta": {"severity": "high"},
        "noise": "random"
    }

    result = handle_outliers({}, diag)

    assert result["column"] == "A"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 20}},
        "meta": {"severity": "high"}
    }

    r1 = handle_outliers({}, diag)
    r2 = handle_outliers({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_invalid_severity_value():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": 20}},
        "meta": {"severity": "critical"}
    }

    result = handle_outliers({}, diag)

    assert result is None


def test_non_numeric_outlier_pct():
    diag = {
        "column": "A",
        "data": {"details": {"outlier_pct": "invalid"}},
        "meta": {"severity": "high"}
    }

    result = handle_outliers({}, diag)

    # No crash, but weird output allowed
    assert "invalid%" in result["reason"]


def test_non_string_column():
    diag = {
        "column": 123,
        "data": {"details": {"outlier_pct": 20}},
        "meta": {"severity": "high"}
    }

    result = handle_outliers({}, diag)

    assert result["column"] == 123