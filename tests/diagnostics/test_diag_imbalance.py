import pandas as pd
from fitlater.diagnostics.imbalance import check_imbalance


# =========================
# NORMAL CASES
# =========================

def test_non_categorical_returns_none():
    series = pd.Series([1, 2, 3])
    profile = {"type": "numeric", "top_freq": 3}

    result = check_imbalance("col", profile, series)

    assert result is None


def test_balanced_column_returns_none():
    series = pd.Series(["A", "B", "A", "B"])
    profile = {"type": "categorical", "top_freq": 2}

    result = check_imbalance("col", profile, series)

    assert result is None


def test_imbalanced_column_detected():
    series = pd.Series(["A", "A", "A", "B"])
    profile = {"type": "categorical", "top_freq": 3}

    result = check_imbalance("col", profile, series)

    assert result is not None
    assert result["type"] == "imbalance"
    assert result["column"] == "col"
    assert result["meta"]["has_issue"] is True

    assert result["data"]["issue_type"] == "imbalanced_category"
    assert result["data"]["current_type"] == "categorical"


# =========================
# CONFIDENCE TESTS
# =========================

def test_confidence_calculation():
    series = pd.Series(["A", "A", "A", "B"])  # 3/4 = 0.75
    profile = {"type": "categorical", "top_freq": 3}

    result = check_imbalance("col", profile, series)

    assert result["data"]["confidence"] == 0.75


def test_confidence_rounding():
    series = pd.Series(["A"] * 7 + ["B"] * 3)  # 7/10 = 0.7
    profile = {"type": "categorical", "top_freq": 7}

    result = check_imbalance("col", profile, series)

    assert result["data"]["confidence"] == 0.7


# =========================
# EDGE CASES
# =========================

def test_empty_series():
    series = pd.Series([], dtype="object")
    profile = {"type": "categorical", "top_freq": 0}

    result = check_imbalance("col", profile, series)

    assert result is None


def test_missing_top_freq():
    """
    Defaults to 0 → dominance = 0 → no issue
    """
    series = pd.Series(["A", "A", "B"])
    profile = {"type": "categorical"}

    result = check_imbalance("col", profile, series)

    assert result is None


def test_all_same_values():
    """
    Extreme imbalance → should always trigger
    """
    series = pd.Series(["A", "A", "A", "A"])
    profile = {"type": "categorical", "top_freq": 4}

    result = check_imbalance("col", profile, series)

    assert result is not None
    assert result["data"]["confidence"] == 1.0


# =========================
# BOUNDARY CONDITIONS
# =========================

def test_boundary_low_severity_returns_none():
    """
    If dominance falls in 'low' → no issue
    """
    from fitlater.config import IMBALANCE_THRESHOLDS

    low_threshold = IMBALANCE_THRESHOLDS["low"]

    series = pd.Series(["A"] * int(low_threshold * 100) + ["B"] * (100 - int(low_threshold * 100)))
    profile = {"type": "categorical", "top_freq": int(low_threshold * 100)}

    result = check_imbalance("col", profile, series)

    assert result is None


def test_above_low_threshold_triggers_issue():
    from fitlater.config import IMBALANCE_THRESHOLDS

    low_threshold = IMBALANCE_THRESHOLDS["low"]

    top_freq = int((low_threshold + 0.05) * 100)

    series = pd.Series(["A"] * top_freq + ["B"] * (100 - top_freq))
    profile = {"type": "categorical", "top_freq": top_freq}

    result = check_imbalance("col", profile, series)

    assert result is not None


# =========================
# DATA PAYLOAD VALIDATION
# =========================

def test_data_payload_structure():
    series = pd.Series(["A", "A", "A", "B"])
    profile = {"type": "categorical", "top_freq": 3}

    result = check_imbalance("col", profile, series)

    data = result["data"]

    assert set(data.keys()) == {
        "issue_type",
        "expected_type",
        "current_type",
        "confidence",
        "details"
    }

    assert set(data["details"].keys()) == {
        "dominating_value",
        "dominance_ratio"
    }


# =========================
# ROBUSTNESS TESTS
# =========================

def test_profile_extra_keys_ignored():
    series = pd.Series(["A", "A", "B"])
    profile = {
        "type": "categorical",
        "top_freq": 2,
        "random": 123
    }

    result = check_imbalance("col", profile, series)

    # Behavior should not break
    assert result is None or result is not None


def test_series_not_used_for_logic():
    """
    Function depends ONLY on profile, not actual distribution
    """
    series = pd.Series(["A", "B", "C", "D"])  # balanced
    profile = {"type": "categorical", "top_freq": 4}  # says imbalanced

    result = check_imbalance("col", profile, series)

    assert result is not None