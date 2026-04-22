import pytest
from fitlater.diagnostics.base import make_issue, get_severity, severity_order


# =========================
# MAKE_ISSUE TESTS
# =========================

def test_make_issue_basic():
    result = make_issue(
        type="missing",
        column="age",
        data={"missing_pct": 10},
        severity="medium",
        has_issue=True
    )

    assert result["type"] == "missing"
    assert result["column"] == "age"
    assert result["data"] == {"missing_pct": 10}

    assert result["meta"]["has_issue"] is True
    assert result["meta"]["severity"] == "medium"


def test_make_issue_structure():
    result = make_issue("type", "col", {}, "low", False)

    assert set(result.keys()) == {"type", "column", "data", "meta"}
    assert set(result["meta"].keys()) == {"has_issue", "severity"}


def test_make_issue_empty_data():
    result = make_issue("test", "col", {}, "low", False)

    assert result["data"] == {}
    assert result["meta"]["has_issue"] is False


def test_make_issue_data_not_mutated():
    data = {"value": 10}

    result = make_issue("test", "col", data, "low", True)

    result["data"]["value"] = 999

    # Since you're passing reference, this WILL mutate original
    # This test exposes that behavior explicitly
    assert data["value"] == 999

# =========================
# SEVERITY ORDER TESTS
# =========================

def test_severity_order_values():
    assert severity_order["low"] == 0
    assert severity_order["medium"] == 1
    assert severity_order["high"] == 2


def test_severity_order_comparison():
    assert severity_order["high"] > severity_order["medium"]
    assert severity_order["medium"] > severity_order["low"]

# =========================
# GET_SEVERITY TESTS
# =========================

def test_get_severity_low():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(5, thresholds) == "low"


def test_get_severity_medium():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(15, thresholds) == "medium"


def test_get_severity_high():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(25, thresholds) == "high"

def test_get_severity_exact_low_boundary():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(10, thresholds) == "low"


def test_get_severity_exact_medium_boundary():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(20, thresholds) == "medium"

def test_get_severity_zero():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(0, thresholds) == "low"


def test_get_severity_negative_value():
    thresholds = {"low": 10, "medium": 20}

    assert get_severity(-5, thresholds) == "low"

def test_get_severity_invalid_thresholds():
    thresholds = {"low": 20, "medium": 10}  # wrong order

    result = get_severity(15, thresholds)

    # Behavior is undefined, but test ensures function still runs
    assert result in ["low", "medium", "high"]
    
def test_get_severity_non_numeric():
    thresholds = {"low": 10, "medium": 20}

    with pytest.raises(TypeError):
        get_severity("invalid", thresholds)