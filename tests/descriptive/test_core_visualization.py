# test_visualization.py

import pandas as pd
import numpy as np
import pytest

from fitlater.core.visualization import (
    getHistogramData,
    getBoxPlotData,
    getBarChartData,
    getPieChartData,
    getBooleanChartData,
    getTimeSeriesData
)


# -----------------------------
# HISTOGRAM TESTS
# -----------------------------

def test_histogram_basic():
    s = pd.Series([1, 2, 3, 4, 5])
    result = getHistogramData(s)

    assert result["type"] == "histogram"
    assert len(result["counts"]) > 0
    assert len(result["bins"]) == len(result["counts"]) + 1


def test_histogram_empty():
    s = pd.Series([])
    result = getHistogramData(s)

    assert result is None


def test_histogram_with_nan():
    s = pd.Series([1, 2, np.nan, 3])
    result = getHistogramData(s)

    assert result is not None


# -----------------------------
# BOXPLOT TESTS
# -----------------------------

def test_boxplot_basic():
    s = pd.Series([1, 2, 3, 4, 5])
    result = getBoxPlotData(s)

    assert result["type"] == "boxplot"
    assert result["min"] == 1
    assert result["max"] == 5
    assert result["median"] == 3


def test_boxplot_empty():
    s = pd.Series([])
    result = getBoxPlotData(s)

    assert result is None


def test_boxplot_with_nan():
    s = pd.Series([1, 2, np.nan, 3])
    result = getBoxPlotData(s)

    assert result is not None


# -----------------------------
# BAR CHART TESTS
# -----------------------------

def test_bar_chart_basic():
    s = pd.Series(["A", "A", "B", "C"])
    result = getBarChartData(s, top_n=2)

    assert result["type"] == "bar"
    assert len(result["data"]) <= 2


def test_bar_chart_meta_full():
    s = pd.Series(["A", "B", "C"])
    result = getBarChartData(s, top_n=10)

    assert "All" in result["meta"]


def test_bar_chart_meta_partial():
    s = pd.Series(list("ABCDEFGHIJK"))
    result = getBarChartData(s, top_n=5)

    assert "Top" in result["meta"]


def test_bar_chart_empty():
    s = pd.Series([])
    result = getBarChartData(s)

    assert result is None


# -----------------------------
# PIE CHART TESTS
# -----------------------------

def test_pie_chart_basic():
    s = pd.Series(["A", "A", "B"])
    result = getPieChartData(s)

    assert result["type"] == "pie"
    assert isinstance(result["data"], dict)


def test_pie_chart_limit():
    s = pd.Series(list("ABCDEFGHIJK"))
    result = getPieChartData(s, top_n=5)

    assert len(result["data"]) <= 5


def test_pie_chart_empty():
    s = pd.Series([])
    result = getPieChartData(s)

    assert result is None


# -----------------------------
# BOOLEAN TESTS
# -----------------------------

def test_boolean_chart():
    s = pd.Series([True, False, True])
    result = getBooleanChartData(s)

    assert result["type"] == "bar"
    assert "True" in result["data"] or "False" in result["data"]


def test_boolean_empty():
    s = pd.Series([])
    result = getBooleanChartData(s)

    assert result is None


# -----------------------------
# TIME SERIES TESTS
# -----------------------------

def test_time_series_basic():
    s = pd.Series([
        "2020-01-01",
        "2020-01-01",
        "2020-01-02"
    ])

    result = getTimeSeriesData(s)

    assert result["type"] == "line"
    assert len(result["labels"]) == len(result["values"])


def test_time_series_empty():
    s = pd.Series([])
    result = getTimeSeriesData(s)

    assert result is None


# -----------------------------
# STRESS / BREAK TESTS
# -----------------------------

def test_high_cardinality_bar():
    s = pd.Series([f"cat_{i}" for i in range(1000)])
    result = getBarChartData(s, top_n=10)

    assert len(result["data"]) <= 10


def test_large_numeric_histogram():
    s = pd.Series(np.random.randn(10000))
    result = getHistogramData(s)

    assert result is not None


def test_mixed_type_series():
    s = pd.Series([1, "A", True, None])
    
    # Should not crash
    try:
        getBarChartData(s)
    except Exception:
        pytest.fail("Function crashed on mixed types")


def test_all_nan_series():
    s = pd.Series([np.nan, np.nan])
    
    assert getHistogramData(s) is None
    assert getBarChartData(s) is None
    assert getPieChartData(s) is None


# -----------------------------
# CONTRACT TESTS (IMPORTANT)
# -----------------------------

def test_output_keys_histogram():
    s = pd.Series([1, 2, 3])
    result = getHistogramData(s)

    assert set(result.keys()) == {"type", "bins", "counts"}


def test_output_keys_bar():
    s = pd.Series(["A", "B"])
    result = getBarChartData(s)

    assert "type" in result
    assert "data" in result
    assert "meta" in result


def test_output_keys_pie():
    s = pd.Series(["A", "B"])
    result = getPieChartData(s)

    assert "type" in result
    assert "data" in result
    assert "meta" in result