'''
This module is used by the frontend to visualize columns.
The data is aggregated here and prepared for visualizations in 
the frontend
'''
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
    series = series.dropna()

    if series.empty:
        return None

    series = pd.to_datetime(series, errors='coerce').dropna()

    counts = series.dt.date.value_counts().sort_index()

    return {
        "type": "line",
        "labels": [str(d) for d in counts.index],
        "values": counts.tolist()
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

    series = pd.to_datetime(series, errors='coerce').dropna()

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