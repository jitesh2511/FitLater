import pytest
from fitlater.advisory.correlation import handle_corr


# =========================
# NORMAL CASES
# =========================

def test_high_severity_correlation():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.95}},
        "meta": {"severity": "high"}
    }

    result = handle_corr({}, diag)

    assert result["column"] == "A & B"
    assert result["issue_type"] == "correlation"
    assert result["action"] == "Drop one of the correlated columns"
    assert "0.95" in result["reason"]
    assert result["priority"] == 1


def test_medium_severity_correlation():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.7}},
        "meta": {"severity": "medium"}
    }

    result = handle_corr({}, diag)

    assert result["action"] == "Consider feature selection"
    assert result["priority"] == 2


# =========================
# LOW / NO ADVICE
# =========================

def test_low_severity_returns_none():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.3}},
        "meta": {"severity": "low"}
    }

    result = handle_corr({}, diag)

    assert result is None


def test_missing_severity_returns_none():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.8}},
        "meta": {}
    }

    result = handle_corr({}, diag)

    assert result is None


# =========================
# EDGE CASES
# =========================

def test_negative_correlation():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": -0.9}},
        "meta": {"severity": "high"}
    }

    result = handle_corr({}, diag)

    # abs() applied
    assert "0.9" in result["reason"]


def test_zero_correlation_high_severity():
    """
    Inconsistent input: 0 correlation but severity high
    Advisory trusts diagnostics
    """
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.0}},
        "meta": {"severity": "high"}
    }

    result = handle_corr({}, diag)

    assert result is not None
    assert "0.0" in result["reason"]


# =========================
# FAILURE CASES
# =========================

def test_missing_column_key():
    diag = {
        "data": {"details": {"correlation": 0.9}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_corr({}, diag)


def test_missing_column_fields():
    diag = {
        "column": {},
        "data": {"details": {"correlation": 0.9}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_corr({}, diag)


def test_missing_data_key():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_corr({}, diag)


def test_missing_correlation():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_corr({}, diag)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    profile = {"random": 123}
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.8}},
        "meta": {"severity": "high"}
    }

    result = handle_corr(profile, diag)

    assert result["column"] == "A & B"


def test_extra_diag_keys_ignored():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.8}},
        "meta": {"severity": "high"},
        "noise": "random"
    }

    result = handle_corr({}, diag)

    assert result["column"] == "A & B"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.8}},
        "meta": {"severity": "high"}
    }

    r1 = handle_corr({}, diag)
    r2 = handle_corr({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_invalid_severity_value():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": 0.8}},
        "meta": {"severity": "critical"}
    }

    result = handle_corr({}, diag)

    assert result is None


def test_non_numeric_correlation():
    diag = {
        "column": {"column_1": "A", "column_2": "B"},
        "data": {"details": {"correlation": "invalid"}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(TypeError):
        handle_corr({}, diag)


def test_non_string_columns():
    diag = {
        "column": {"column_1": 1, "column_2": 2},
        "data": {"details": {"correlation": 0.9}},
        "meta": {"severity": "high"}
    }

    result = handle_corr({}, diag)

    assert result["column"] == "1 & 2"