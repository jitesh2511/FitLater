from fitlater.config import CORRELATION_THRESHOLD, OUTLIER_THRESHOLD
from fitlater.cli.formatter.descriptive import format_results
from fitlater.core.overview import analyze
from fitlater.core.correlation import analyze_correlation
from fitlater.core.outliers import analyze_outliers

import pandas as pd
import numpy as np


def _data():
    np.random.seed(42)

    df = pd.DataFrame({
        "age": np.random.normal(30, 5, 100),
        "income": np.random.exponential(scale=50000, size=100),
        "score": np.append(np.random.randint(50, 100, 95), [np.nan] * 5),
        "is_student": np.random.choice([True, False], 100),
        "city": np.random.choice(["Delhi", "Mumbai", "Chennai"], 100),
        "department": np.append(
            np.random.choice(["HR", "Tech", "Sales"], 95),
            [np.nan] * 5,
        ),
        "join_date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
    })

    return pd.concat([df, df.iloc[:3]], ignore_index=True)


def test_format_results_non_empty():
    data = _data()
    overview = analyze(data)
    correlation = analyze_correlation(data, CORRELATION_THRESHOLD)
    outliers = analyze_outliers(data, OUTLIER_THRESHOLD)

    out = format_results(overview, correlation, outliers)

    assert isinstance(out, str)
    assert len(out) > 0
    assert "Overview" in out
    assert "Correlation Analysis" in out
    assert "Outlier Analysis" in out
