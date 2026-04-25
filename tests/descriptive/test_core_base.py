import pandas as pd
from fitlater.core.base import get_metadata, get_missing


# =========================
# METADATA TESTS
# =========================

def test_metadata_basic():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
    })

    result = get_metadata(df)

    assert result["n_rows"] == 3
    assert result["n_cols"] == 2
    assert isinstance(result["memory"], str)


def test_metadata_empty_df():
    df = pd.DataFrame()

    result = get_metadata(df)

    assert result["n_rows"] == 0
    assert result["n_cols"] == 0
    assert isinstance(result["memory"], str)


def test_metadata_memory_format_bytes():
    df = pd.DataFrame({"A": [1]})  # very small

    result = get_metadata(df)

    assert "B" in result["memory"]


def test_metadata_memory_format_kb():
    df = pd.DataFrame({"A": list(range(1000))})

    result = get_metadata(df)

    # Should be at least KB
    assert "KB" in result["memory"] or "MB" in result["memory"]


def test_metadata_memory_format_mb():
    df = pd.DataFrame({"A": list(range(10**6))})

    result = get_metadata(df)

    assert "MB" in result["memory"]


def test_metadata_keys():
    df = pd.DataFrame({"A": [1, 2]})

    result = get_metadata(df)

    assert set(result.keys()) == {"n_rows", "n_cols", "memory"}


# =========================
# MISSING TESTS
# =========================

def test_missing_basic():
    series = pd.Series([1, None, 3, None])

    result = get_missing(series)

    assert result["missing_count"] == 2
    assert result["missing_pct"] == 50.0


def test_missing_no_missing():
    series = pd.Series([1, 2, 3])

    result = get_missing(series)

    assert result["missing_count"] == 0
    assert result["missing_pct"] == 0.0


def test_missing_all_missing():
    series = pd.Series([None, None, None])

    result = get_missing(series)

    assert result["missing_count"] == 3
    assert result["missing_pct"] == 100.0


def test_missing_empty_series():
    series = pd.Series([], dtype="float")

    result = get_missing(series)

    assert result["missing_count"] == 0
    assert result["missing_pct"] == 0.0


def test_missing_rounding():
    series = pd.Series([1, None, None])  # 2/3 = 66.666...

    result = get_missing(series)

    assert result["missing_pct"] == 66.67


def test_missing_keys():
    series = pd.Series([1, None])

    result = get_missing(series)

    assert set(result.keys()) == {"missing_count", "missing_pct"}