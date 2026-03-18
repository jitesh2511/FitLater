from fitlater.core.overview import analyze as over_analyze
from fitlater.core.correlation import analyze_correlation as corr_analyze
from fitlater.core.outliers import analyze_outliers as out_analyze

from fitlater.cli.formatter import (format_overview, format_correlation, format_outliers, format_results)

from fitlater.config import (CORRELATION_THRESHOLD, OUTLIER_THRESHOLD)

def get_overview(data):
    return format_overview(over_analyze(data))

def get_correlation(data):
    return format_correlation(corr_analyze(data, CORRELATION_THRESHOLD))

def get_outliers(data):
    return format_outliers(out_analyze(data, OUTLIER_THRESHOLD))

def get_results(data):
    return format_results(over_analyze(data), corr_analyze(data, CORRELATION_THRESHOLD), out_analyze(data, OUTLIER_THRESHOLD))