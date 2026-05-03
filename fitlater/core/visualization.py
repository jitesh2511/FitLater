"""
Lightweight visualization data helpers.

Prepares aggregated data structures (histogram, boxplot, bar, pie,
time series) suitable for rendering in a frontend. Functions return
small JSON-like dicts describing chart type and values, or `None` for
empty inputs.
"""
import pandas as pd
import numpy as np

def getHistogramData(series, bins=20):
    series = series.dropna()

    if series.empty:
        return None

    counts, bin_edges = np.histogram(series, bins=bins)

    return {
        "type": "histogram",
        "bins": bin_edges.tolist(),
        "counts": counts.tolist()
    }

def getBoxPlotData(series):
    series = series.dropna()

    if series.empty:
        return None

    q1 = series.quantile(0.25)
    q2 = series.quantile(0.5)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = max(series.min(), q1 - 1.5 * iqr)
    upper = min(series.max(), q3 + 1.5 * iqr)

    return {
        "type": "boxplot",
        "min": float(series.min()),
        "q1": float(q1),
        "median": float(q2),
        "q3": float(q3),
        "max": float(series.max()),
        "lower_bound": float(lower),
        "upper_bound": float(upper)
    }

def getBarChartData(series, top_n=10):
    series = series.dropna()

    if series.empty:
        return None

    counts = series.value_counts().head(top_n)
    total_unique = series.nunique()
    shown = len(counts)

    if total_unique > top_n:
        meta = f"Top {shown} of {total_unique} categories shown"
    else:
        meta = f"All {shown} categories shown"

    data = {str(k): int(v) for k, v in counts.items()}

    return {
        "type": "bar",
        "data": data,
        "meta": meta
    }

def getPieChartData(series, top_n=5):
    series = series.dropna()

    if series.empty:
        return None

    counts = series.value_counts().head(top_n)
    total_unique = series.nunique()
    shown = len(counts)

    if total_unique > top_n:
        meta = f"Top {shown} of {total_unique} categories shown"
    else:
        meta = f"All {shown} categories shown"

    data = {str(k): int(v) for k, v in counts.items()}

    return {
        "type": "pie",
        "data": data,
        "meta": meta
    }

def getBooleanChartData(series):
    series = series.dropna()

    if series.empty:
        return None

    counts = series.value_counts()

    return {
        "type": "bar",
        "data": {str(k): int(v) for k, v in counts.items()}
    }

def getTimeSeriesData(series):
    import pandas as pd

    series = pd.to_datetime(series, errors='coerce', format='mixed').dropna()

    if series.empty:
        return None

    n_unique = series.nunique()

    # 🔥 Adaptive aggregation
    if n_unique > 300:
        # group by MONTH
        grouped = series.dt.to_period("M").value_counts().sort_index()
        labels = [str(p) for p in grouped.index]

    elif n_unique > 50:
        # group by DAY
        grouped = series.dt.date.value_counts().sort_index()
        labels = [str(d) for d in grouped.index]

    else:
        # small data → no aggregation
        grouped = series.value_counts().sort_index()
        labels = [str(d) for d in grouped.index]

    return {
        "type": "line",
        "labels": labels,
        "values": grouped.tolist()
    }

def getBooleanPieChartData(series):
    series = series.dropna()

    if series.empty:
        return None

    counts = series.value_counts()

    return {
        "type": "pie",
        "data": {str(k): int(v) for k, v in counts.items()}
    }

def getDatetimeWeekdayDistribution(series):
    import pandas as pd

    series = pd.to_datetime(series, errors='coerce', format='mixed').dropna()

    if series.empty:
        return None

    counts = series.dt.day_name().value_counts()

    # Order properly
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    counts = counts.reindex(order).dropna()

    return {
        "type": "bar",
        "labels": counts.index.tolist(),
        "values": counts.tolist()
    }