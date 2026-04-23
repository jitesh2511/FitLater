import pytest
from fitlater.advisory.type_issues import handle_type_issue


# =========================
# NORMAL CASES
# =========================

def test_numeric_as_string_high():
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "high"}
    }

    result = handle_type_issue({}, diag)

    assert result["column"] == "A"
    assert result["issue_type"] == "type_issue"
    assert result["action"] == "Convert column to numeric"
    assert result["priority"] == 1


def test_datetime_as_string_medium():
    diag = {
        "column": "A",
        "data": {"issue_type": "datetime_as_string"},
        "meta": {"severity": "medium"}
    }

    result = handle_type_issue({}, diag)

    assert result["action"] == "Convert column to datetime"
    assert result["priority"] == 2


def test_mixed_types():
    diag = {
        "column": "A",
        "data": {"issue_type": "mixed_types"},
        "meta": {"severity": "medium"}
    }

    result = handle_type_issue({}, diag)

    assert result["action"] == "Clean inconsistent values"


def test_boolean_as_string():
    diag = {
        "column": "A",
        "data": {"issue_type": "boolean_as_string"},
        "meta": {"severity": "medium"}
    }

    result = handle_type_issue({}, diag)

    assert result["action"] == "Convert to boolean"


# =========================
# SEVERITY TESTS
# =========================

def test_low_severity_returns_none():
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "low"}
    }

    result = handle_type_issue({}, diag)

    assert result is None


def test_missing_severity_returns_none():
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {}
    }

    result = handle_type_issue({}, diag)

    assert result is None


# =========================
# EDGE CASES
# =========================

def test_unknown_issue_type():
    diag = {
        "column": "A",
        "data": {"issue_type": "unknown_type"},
        "meta": {"severity": "high"}
    }

    result = handle_type_issue({}, diag)

    assert result is None


def test_missing_issue_type():
    diag = {
        "column": "A",
        "data": {},
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_type_issue({}, diag)


def test_missing_data_key():
    diag = {
        "column": "A",
        "meta": {"severity": "high"}
    }

    with pytest.raises(KeyError):
        handle_type_issue({}, diag)


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    profile = {"random": 123}
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "high"}
    }

    result = handle_type_issue(profile, diag)

    assert result["column"] == "A"


def test_extra_diag_keys_ignored():
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "high"},
        "noise": "random"
    }

    result = handle_type_issue({}, diag)

    assert result["column"] == "A"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "high"}
    }

    r1 = handle_type_issue({}, diag)
    r2 = handle_type_issue({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_invalid_severity_value():
    diag = {
        "column": "A",
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "critical"}
    }

    result = handle_type_issue({}, diag)

    assert result is None


def test_non_string_issue_type():
    diag = {
        "column": "A",
        "data": {"issue_type": 123},
        "meta": {"severity": "high"}
    }

    result = handle_type_issue({}, diag)

    assert result is None


def test_non_string_column():
    diag = {
        "column": 123,
        "data": {"issue_type": "numeric_as_string"},
        "meta": {"severity": "high"}
    }

    result = handle_type_issue({}, diag)

    assert result["column"] == 123