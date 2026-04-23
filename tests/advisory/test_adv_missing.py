import pytest
from fitlater.advisory.missing import handle_missing


# =========================
# HIGH SEVERITY CASE
# =========================

def test_high_severity_drop_column():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 80}},
        "meta": {"severity": "high"}
    }

    profile = {"A": {"type": "numeric"}}

    result = handle_missing(profile, diag)

    assert result["column"] == "A"
    assert result["issue_type"] == "missing"
    assert result["action"] == "Drop column"
    assert "80%" in result["reason"]
    assert result["priority"] == 1


# =========================
# MEDIUM / LOW SEVERITY (IMPUTATION)
# =========================

def test_median_strategy():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 20}},
        "meta": {"severity": "medium"}
    }

    profile = {"A": {"type": "numeric", "skew": 2.0}}

    result = handle_missing(profile, diag)

    assert result["action"] == "Fill with median"
    assert "skewed" in result["reason"]
    assert result["priority"] == 2


def test_mean_strategy():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 10}},
        "meta": {"severity": "medium"}
    }

    profile = {"A": {"type": "numeric", "skew": 0.2}}

    result = handle_missing(profile, diag)

    assert result["action"] == "Fill with mean"


def test_mode_strategy():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 15}},
        "meta": {"severity": "medium"}
    }

    profile = {"A": {"type": "categorical"}}

    result = handle_missing(profile, diag)

    assert result["action"] == "Fill with mode"


# =========================
# EDGE CASES
# =========================

def test_missing_severity_none():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 20}},
        "meta": {}
    }

    profile = {"A": {"type": "numeric"}}

    result = handle_missing(profile, diag)

    # falls into imputation branch
    assert result is not None


def test_missing_profile_column():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 20}},
        "meta": {"severity": "medium"}
    }

    profile = {}  # missing column

    with pytest.raises(KeyError):
        handle_missing(profile, diag)


def test_missing_details_key():
    diag = {
        "column": "A",
        "data": {},
        "meta": {"severity": "high"}
    }

    profile = {"A": {"type": "numeric"}}

    with pytest.raises(KeyError):
        handle_missing(profile, diag)


def test_missing_pct_not_numeric():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": "invalid"}},
        "meta": {"severity": "high"}
    }

    profile = {"A": {"type": "numeric"}}

    result = handle_missing(profile, diag)

    # No crash, but string will appear in reason
    assert "invalid%" in result["reason"]


# =========================
# STRATEGY DEPENDENCY TEST
# =========================

def test_strategy_called_correctly(monkeypatch):
    """
    Ensure get_imputation_strategy is used correctly
    """
    def fake_strategy(_):
        return "median"

    from fitlater.advisory import missing as module

    monkeypatch.setattr(module, "get_imputation_strategy", fake_strategy)

    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 10}},
        "meta": {"severity": "medium"}
    }

    profile = {"A": {"type": "numeric"}}

    result = handle_missing(profile, diag)

    assert result["action"] == "Fill with median"


# =========================
# ROBUSTNESS TESTS
# =========================

def test_extra_diag_keys_ignored():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 20}},
        "meta": {"severity": "medium"},
        "noise": "random"
    }

    profile = {"A": {"type": "numeric"}}

    result = handle_missing(profile, diag)

    assert result["column"] == "A"


def test_non_string_column():
    diag = {
        "column": 123,
        "data": {"details": {"missing_pct": 20}},
        "meta": {"severity": "medium"}
    }

    profile = {123: {"type": "numeric"}}

    result = handle_missing(profile, diag)

    assert result["column"] == 123


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "column": "A",
        "data": {"details": {"missing_pct": 20}},
        "meta": {"severity": "medium"}
    }

    profile = {"A": {"type": "numeric"}}

    r1 = handle_missing(profile, diag)
    r2 = handle_missing(profile, diag)

    assert r1 == r2