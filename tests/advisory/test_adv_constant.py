import pytest
from fitlater.advisory.constant_column import handle_constant


# =========================
# NORMAL CASES
# =========================

def test_basic_constant_advice():
    profile = {}
    diag = {
        "column": "A",
        "type": "constant"
    }

    result = handle_constant(profile, diag)

    assert result["column"] == "A"
    assert result["issue_type"] == "constant"

    assert result["action"] == "Drop column"
    assert "no predictive power" in result["reason"]

    assert result["priority"] == 1


# =========================
# CONTRACT VALIDATION
# =========================

def test_output_structure():
    profile = {}
    diag = {"column": "A"}

    result = handle_constant(profile, diag)

    expected_keys = {
        "column",
        "issue_type",
        "action",
        "reason",
        "priority"
    }

    assert set(result.keys()) == expected_keys


# =========================
# EDGE CASES
# =========================

def test_missing_column_key():
    profile = {}
    diag = {}

    with pytest.raises(KeyError):
        handle_constant(profile, diag)


def test_column_none():
    profile = {}
    diag = {"column": None}

    result = handle_constant(profile, diag)

    # Should still return valid structure
    assert result["column"] is None


def test_empty_column_name():
    profile = {}
    diag = {"column": ""}

    result = handle_constant(profile, diag)

    assert result["column"] == ""


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_unused():
    """
    Profile is not used → should not affect output
    """
    profile = {"random": 123}
    diag = {"column": "A"}

    result = handle_constant(profile, diag)

    assert result["column"] == "A"


def test_extra_diag_keys_ignored():
    diag = {
        "column": "A",
        "type": "constant",
        "random": "noise"
    }

    result = handle_constant({}, diag)

    assert result["column"] == "A"


# =========================
# CONSISTENCY TESTS
# =========================

def test_same_input_same_output():
    diag = {"column": "A"}

    r1 = handle_constant({}, diag)
    r2 = handle_constant({}, diag)

    assert r1 == r2


# =========================
# BREAK TESTS (IMPORTANT)
# =========================

def test_wrong_diag_type_still_returns():
    """
    Advisory should not rely on diag['type']
    """
    diag = {"column": "A", "type": "missing"}

    result = handle_constant({}, diag)

    # Still produces constant advice (module-specific)
    assert result["issue_type"] == "constant"


def test_invalid_diag_structure():
    """
    diag is not dict → should fail
    """
    with pytest.raises(TypeError):
        handle_constant({}, None)


def test_non_string_column():
    diag = {"column": 123}

    result = handle_constant({}, diag)

    assert result["column"] == 123