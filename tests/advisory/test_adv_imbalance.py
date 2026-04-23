import pytest
from fitlater.advisory.imbalance import handle_imbalance


# =========================
# NORMAL CASES
# =========================

def test_high_severity_imbalance():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.9}},
        "meta": {"severity": "high"}
    }

    result = handle_imbalance({}, diag)

    assert result["column"] == "target"
    assert result["issue_type"] == "imbalance"
    assert result["action"] == "Consider resampling (SMOTE, undersampling)"
    assert "90.0% dominance" in result["reason"]
    assert result["priority"] == 1


def test_medium_severity_imbalance():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.65}},
        "meta": {"severity": "medium"}
    }

    result = handle_imbalance({}, diag)

    assert result["action"] == "Monitor imbalance or use class weights"
    assert "65.0% dominance" in result["reason"]
    assert result["priority"] == 2


# =========================
# LOW / NO ADVICE
# =========================

def test_low_severity_returns_none():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.4}},
        "meta": {"severity": "low"}
    }

    result = handle_imbalance({}, diag)

    assert result is None


def test_missing_severity_returns_none():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.8}},
        "meta": {}
    }

    result = handle_imbalance({}, diag)

    assert result is None


# =========================
# EDGE CASES
# =========================

def test_extreme_imbalance_100_percent():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 1.0}},
        "meta": {"severity": "high"}
    }

    result = handle_imbalance({}, diag)

    assert "100.0% dominance" in result["reason"]


def test_zero_imbalance_high_severity():
    """
    Inconsistent input: dominance 0 but severity high
    Advisory should trust diagnostics
    """
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.0}},
        "meta": {"severity": "high"}
    }

    result = handle_imbalance({}, diag)

    assert result is not None
    assert "0.0% dominance" in result["reason"]


# =========================
# PRECISION TESTS
# =========================

def test_precision_rounding():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.66666}},
        "meta": {"severity": "medium"}
    }

    result = handle_imbalance({}, diag)

    # 0.66666 * 100 → 66.7%
    assert "66.7% dominance" in result["reason"]


# =========================
# FAILURE CASES
# =========================

def test_missing_data_key():
    diag = {
        "column": "target",
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_imbalance({}, diag)


def test_missing_details_key():
    diag = {
        "column": "target",
        "data": {},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_imbalance({}, diag)


def test_missing_dominance_ratio():
    diag = {
        "column": "target",
        "data": {"details": {}},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_imbalance({}, diag)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    profile = {"random": 123}
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.8}},
        "meta": {"severity": "high"}
    }

    result = handle_imbalance(profile, diag)

    assert result["column"] == "target"


def test_extra_diag_keys_ignored():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.8}},
        "meta": {"severity": "high"},
        "noise": "random"
    }

    result = handle_imbalance({}, diag)

    assert result["column"] == "target"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.8}},
        "meta": {"severity": "high"}
    }

    r1 = handle_imbalance({}, diag)
    r2 = handle_imbalance({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_invalid_severity_value():
    diag = {
        "column": "target",
        "data": {"details": {"dominance_ratio": 0.8}},
        "meta": {"severity": "critical"}  # invalid
    }

    result = handle_imbalance({}, diag)

    assert result is None


def test_non_string_column():
    diag = {
        "column": 123,
        "data": {"details": {"dominance_ratio": 0.8}},
        "meta": {"severity": "high"}
    }

    result = handle_imbalance({}, diag)

    assert result["column"] == 123