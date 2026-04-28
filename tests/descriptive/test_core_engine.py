import pytest
import pandas as pd
from fitlater.core.engine import build_description


# =========================
# EMPTY DATAFRAME
# =========================

def test_build_description_empty_df():
    df = pd.DataFrame()

    result = build_description(df)

    assert result["meta"]["n_rows"] == 0
    assert result["meta"]["n_cols"] == 0
    assert result["profile"] == {}
    assert result["column_types"] == {}


# =========================
# BASIC INTEGRATION TEST
# =========================

def test_build_description_basic():
    df = pd.DataFrame({
        "num": [1, 2, 3],
        "cat": ["A", "B", "A"],
        "bool": [True, False, True]
    })

    result = build_description(df)

    # Structure
    assert "meta" in result
    assert "profile" in result
    assert "column_types" in result

    # Column types
    assert result["column_types"]["num"] == "numeric"
    assert result["column_types"]["cat"] == "categorical"
    assert result["column_types"]["bool"] == "boolean"

    # Profile exists
    assert "num" in result["profile"]
    assert "cat" in result["profile"]
    assert "bool" in result["profile"]


# =========================
# NUMERIC COLUMN PROFILE
# =========================

def test_numeric_profile():
    df = pd.DataFrame({"num": [1, 2, 3, 4]})

    result = build_description(df)

    profile = result["profile"]["num"]

    assert "mean" in profile
    assert "median" in profile
    assert "missing_count" in profile


# =========================
# CATEGORICAL + IDENTIFIER
# =========================

def test_categorical_and_identifier_share_stats():
    df = pd.DataFrame({
        "cat": ["A", "B", "A"],
        "id": ["u1", "u2", "u3"]
    })

    result = build_description(df)

    cat_profile = result["profile"]["cat"]
    id_profile = result["profile"]["id"]

    # Both use categorical stats
    for key in ["n_unique", "top_value", "top_freq"]:
        assert key in cat_profile
        assert key in id_profile


# =========================
# DATETIME COLUMN
# =========================

def test_datetime_profile():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02"])
    })

    result = build_description(df)

    profile = result["profile"]["date"]

    assert "min" in profile
    assert "max" in profile
    assert "nunique" in profile


# =========================
# MIXED COLUMN
# =========================

def test_mixed_profile():
    df = pd.DataFrame({
        "mixed": [1, "A", 2]
    })

    result = build_description(df)

    assert result["column_types"]["mixed"] == "mixed"

    profile = result["profile"]["mixed"]

    assert "n_mixed_types" in profile


# =========================
# EMPTY COLUMN PROFILE
# =========================

def test_empty_column_profile():
    df = pd.DataFrame({
        "empty": [None, None]
    })

    result = build_description(df)

    assert result["column_types"]["empty"] == "empty"

    profile = result["profile"]["empty"]

    # Only missing stats should exist
    assert "missing_count" in profile
    assert "missing_pct" in profile
    assert len(profile) == 4


# =========================
# MISSING VALUES MERGING
# =========================

def test_missing_stats_always_present():
    df = pd.DataFrame({
        "num": [1, None, 3],
        "cat": ["A", None, "B"]
    })

    result = build_description(df)

    for col in df.columns:
        profile = result["profile"][col]
        assert "missing_count" in profile
        assert "missing_pct" in profile


# =========================
# OUTPUT CONSISTENCY
# =========================

def test_profile_keys_match_columns():
    df = pd.DataFrame({
        "A": [1],
        "B": ["x"]
    })

    result = build_description(df)

    assert set(result["profile"].keys()) == set(df.columns)
    assert set(result["column_types"].keys()) == set(df.columns)


# =========================
# NO MUTATION OF INPUT DF
# =========================

def test_input_dataframe_not_modified():
    df = pd.DataFrame({
        "A": [1, 2, 3]
    })

    df_copy = df.copy()

    build_description(df)

    pd.testing.assert_frame_equal(df, df_copy)