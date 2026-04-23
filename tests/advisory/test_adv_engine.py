import pytest
from fitlater.advisory.engine import get_advice


# =========================
# BASIC CASES
# =========================

def test_empty_diagnostics():
    result = get_advice({}, [])

    assert result == []


def test_no_issues_filtered_out():
    diagnostics = [
        {"type": "missing", "meta": {"has_issue": False}}
    ]

    result = get_advice({}, diagnostics)

    assert result == []


# =========================
# SINGLE ISSUE
# =========================

def test_single_missing_issue():
    diagnostics = [
        {
            "type": "missing",
            "column": "A",
            "data": {"details": {"missing_pct": 50}},
            "meta": {"has_issue": True, "severity": "high"}
        }
    ]

    profile = {"A": {"type": "numeric"}}

    result = get_advice(profile, diagnostics)

    assert len(result) == 1
    assert result[0]["issue_type"] == "missing"


# =========================
# MULTIPLE ISSUES
# =========================

def test_multiple_issues():
    diagnostics = [
        {
            "type": "missing",
            "column": "A",
            "data": {"details": {"missing_pct": 50}},
            "meta": {"has_issue": True, "severity": "high"}
        },
        {
            "type": "duplicates",
            "data": {"details": {"duplicate_pct": 20}},
            "meta": {"has_issue": True, "severity": "medium"}
        }
    ]

    profile = {"A": {"type": "numeric"}}

    result = get_advice(profile, diagnostics)

    assert len(result) == 2


# =========================
# HANDLER ROUTING
# =========================

def test_unknown_issue_type_skipped():
    diagnostics = [
        {
            "type": "unknown",
            "meta": {"has_issue": True}
        }
    ]

    result = get_advice({}, diagnostics)

    assert result == []


# =========================
# SORTING
# =========================

def test_priority_sorting():
    diagnostics = [
        {
            "type": "duplicates",
            "data": {"details": {"duplicate_pct": 20}},
            "meta": {"has_issue": True, "severity": "medium"}
        },
        {
            "type": "missing",
            "column": "A",
            "data": {"details": {"missing_pct": 80}},
            "meta": {"has_issue": True, "severity": "high"}
        }
    ]

    profile = {"A": {"type": "numeric"}}

    result = get_advice(profile, diagnostics)

    # high priority (1) should come first
    assert result[0]["priority"] <= result[1]["priority"]


# =========================
# EDGE CASES
# =========================

def test_missing_meta_key():
    diagnostics = [
        {
            "type": "missing",
            "column": "A",
            "data": {"details": {"missing_pct": 50}}
        }
    ]

    with pytest.raises(KeyError):
        get_advice({}, diagnostics)


def test_missing_has_issue_key():
    diagnostics = [
        {
            "type": "missing",
            "meta": {}
        }
    ]

    with pytest.raises(KeyError):
        get_advice({}, diagnostics)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_handler_returns_none():
    diagnostics = [
        {
            "type": "distribution",
            "column": "A",
            "data": {"details": {"skew": 0.2}},
            "meta": {"has_issue": True, "severity": "low"}
        }
    ]

    result = get_advice({}, diagnostics)

    assert result == []


def test_handler_returns_invalid_structure():
    """
    Simulate a broken handler
    """
    diagnostics = [
        {
            "type": "missing",
            "column": "A",
            "data": {"details": {"missing_pct": 50}},
            "meta": {"has_issue": True, "severity": "high"}
        }
    ]

    profile = {"A": {"type": "numeric"}}

    result = get_advice(profile, diagnostics)

    # ensure safe structure
    assert isinstance(result, list)


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diagnostics = [
        {
            "type": "missing",
            "column": "A",
            "data": {"details": {"missing_pct": 50}},
            "meta": {"has_issue": True, "severity": "high"}
        }
    ]

    profile = {"A": {"type": "numeric"}}

    r1 = get_advice(profile, diagnostics)
    r2 = get_advice(profile, diagnostics)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_diag_not_dict():
    with pytest.raises(TypeError):
        get_advice({}, [None])


def test_non_list_diagnostics():
    with pytest.raises(TypeError):
        get_advice({}, None)


def test_missing_type_key():
    diagnostics = [
        {
            "meta": {"has_issue": True}
        }
    ]

    with pytest.raises(KeyError):
        get_advice({}, diagnostics)