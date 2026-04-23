import pytest
from fitlater.advisory.distribution import handle_distribution


# =========================
# NORMAL CASES
# =========================

def test_high_severity_distribution():
    diag = {
        "column": "A",
        "data": {"details": {"skew": 3.5}},
        "meta": {"severity": "high"}
    }

    result = handle_distribution({}, diag)

    assert result["column"] == "A"
    assert result["issue_type"] == "distribution"
    assert result["action"] == "Apply log or Box-Cox transformation"
    assert "skew=3.5" in result["reason"]
    assert result["priority"] == 1


def test_medium_severity_distribution():
    diag = {
        "column": "A",
        "data": {"details": {"skew": 1.8}},
        "meta": {"severity": "medium"}
    }

    result = handle_distribution({}, diag)

    assert result["action"] == "Consider transformation if model is sensitive"
    assert "skew=1.8" in result["reason"]
    assert result["priority"] == 2


# =========================
# LOW SEVERITY (NO ADVICE)
# =========================

def test_low_severity_returns_none():
    diag = {
        "column": "A",
        "data": {"details": {"skew": 0.5}},
        "meta": {"severity": "low"}
    }

    result = handle_distribution({}, diag)

    assert result is None


def test_missing_severity_returns_none():
    diag = {
        "column": "A",
        "data": {"details": {"skew": 2.0}},
        "meta": {}
    }

    result = handle_distribution({}, diag)

    assert result is None


# =========================
# EDGE CASES
# =========================

def test_negative_skew():
    diag = {
        "column": "A",
        "data": {"details": {"skew": -2.3}},
        "meta": {"severity": "high"}
    }

    result = handle_distribution({}, diag)

    # Should still work (absolute skew concept)
    assert "skew=-2.3" in result["reason"]


def test_zero_skew_high_severity():
    """
    Inconsistent input: severity says high, skew is 0
    Advisory should trust diagnostics
    """
    diag = {
        "column": "A",
        "data": {"details": {"skew": 0.0}},
        "meta": {"severity": "high"}
    }

    result = handle_distribution({}, diag)

    assert result is not None


# =========================
# FAILURE CASES (IMPORTANT)
# =========================

def test_missing_data_key():
    diag = {
        "column": "A",
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_distribution({}, diag)


def test_missing_details_key():
    diag = {
        "column": "A",
        "data": {},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_distribution({}, diag)


def test_missing_skew():
    diag = {
        "column": "A",
        "data": {"details": {}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_distribution({}, diag)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    profile = {"random": 123}
    diag = {
        "column": "A",
        "data": {"details": {"skew": 2.0}},
        "meta": {"severity": "high"}
    }

    result = handle_distribution(profile, diag)

    assert result["column"] == "A"


def test_extra_diag_keys_ignored():
    diag = {
        "column": "A",
        "data": {"details": {"skew": 2.0}},
        "meta": {"severity": "high"},
        "noise": "random"
    }

    result = handle_distribution({}, diag)

    assert result["column"] == "A"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "column": "A",
        "data": {"details": {"skew": 2.0}},
        "meta": {"severity": "high"}
    }

    r1 = handle_distribution({}, diag)
    r2 = handle_distribution({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (VERY IMPORTANT)
# =========================

def test_invalid_severity_value():
    """
    Unknown severity should behave like low → no advice
    """
    diag = {
        "column": "A",
        "data": {"details": {"skew": 2.0}},
        "meta": {"severity": "critical"}  # invalid
    }

    result = handle_distribution({}, diag)

    assert result is None


def test_non_string_column():
    diag = {
        "column": 123,
        "data": {"details": {"skew": 2.0}},
        "meta": {"severity": "high"}
    }

    result = handle_distribution({}, diag)

    assert result["column"] == 123


def test_non_numeric_skew():
    diag = {
        "column": "A",
        "data": {"details": {"skew": "invalid"}},
        "meta": {"severity": "high"}
    }

    result = handle_distribution({}, diag)

    # No crash, but reason will include invalid skew
    assert "invalid" in result["reason"]