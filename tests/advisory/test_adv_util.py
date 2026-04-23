import pytest
from fitlater.advisory.util import build_advice


# =========================
# NORMAL CASES
# =========================

def test_basic_advice():
    result = build_advice(
        column="A",
        issue="missing",
        action="Fill with mean",
        reason="Low missing percentage",
        priority=2
    )

    assert result["column"] == "A"
    assert result["issue_type"] == "missing"
    assert result["action"] == "Fill with mean"
    assert result["reason"] == "Low missing percentage"
    assert result["priority"] == 2


# =========================
# CONTRACT VALIDATION
# =========================

def test_output_structure():
    result = build_advice("A", "missing", "action", "reason", 1)

    expected_keys = {
        "column",
        "issue_type",
        "action",
        "reason",
        "priority"
    }

    assert set(result.keys()) == expected_keys


def test_no_extra_keys():
    result = build_advice("A", "missing", "action", "reason", 1)

    assert len(result) == 5


# =========================
# EDGE CASES
# =========================

def test_none_values():
    result = build_advice(None, None, None, None, None)

    assert result["column"] is None
    assert result["issue_type"] is None
    assert result["action"] is None
    assert result["reason"] is None
    assert result["priority"] is None


def test_empty_strings():
    result = build_advice("", "", "", "", 0)

    assert result["column"] == ""
    assert result["issue_type"] == ""
    assert result["action"] == ""
    assert result["reason"] == ""
    assert result["priority"] == 0


# =========================
# TYPE FLEXIBILITY TESTS
# =========================

def test_non_string_column():
    result = build_advice(123, "missing", "action", "reason", 1)

    assert result["column"] == 123


def test_non_string_issue():
    result = build_advice("A", 123, "action", "reason", 1)

    assert result["issue_type"] == 123


def test_non_string_action():
    result = build_advice("A", "missing", 123, "reason", 1)

    assert result["action"] == 123


def test_non_string_reason():
    result = build_advice("A", "missing", "action", 123, 1)

    assert result["reason"] == 123


def test_non_int_priority():
    result = build_advice("A", "missing", "action", "reason", "high")

    assert result["priority"] == "high"


# =========================
# CONSISTENCY TESTS
# =========================

def test_deterministic_output():
    args = ("A", "missing", "action", "reason", 1)

    r1 = build_advice(*args)
    r2 = build_advice(*args)

    assert r1 == r2


# =========================
# MUTABILITY TESTS
# =========================

def test_output_is_independent():
    result = build_advice("A", "missing", "action", "reason", 1)

    result["column"] = "B"

    new_result = build_advice("A", "missing", "action", "reason", 1)

    assert new_result["column"] == "A"


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_missing_arguments():
    with pytest.raises(TypeError):
        build_advice("A", "missing")  # missing args


def test_extra_arguments():
    with pytest.raises(TypeError):
        build_advice("A", "missing", "action", "reason", 1, "extra")


def test_none_function_call():
    with pytest.raises(TypeError):
        build_advice(None)  # incomplete