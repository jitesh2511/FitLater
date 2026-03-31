from fitlater.core.overview import analyze as over_analyze
from fitlater.core.correlation import analyze_correlation as corr_analyze
from fitlater.core.outliers import analyze_outliers as out_analyze

from fitlater.diagnostics.missing import check_missing
from fitlater.diagnostics.correlation import check_correlation
from fitlater.diagnostics.outliers import check_outliers
from fitlater.diagnostics.distribution import check_distribution

from fitlater.cli.formatter.descriptive import (
    format_overview,
    format_correlation, 
    format_outliers, 
    format_results
)
from fitlater.cli.formatter.diagnostics import (
    format_missing_diag, 
    format_corr_diag, 
    format_outliers_diag, 
    format_distribution_diag, 
    format_diagnostics
)

from fitlater.config import (CORRELATION_THRESHOLD, OUTLIER_THRESHOLD)

def get_overview(data):
    return format_overview(over_analyze(data))

def get_correlation(data):
    return format_correlation(corr_analyze(data, CORRELATION_THRESHOLD))

def get_outliers(data):
    return format_outliers(out_analyze(data, OUTLIER_THRESHOLD))

def get_description(data):
    return format_results(over_analyze(data), corr_analyze(data, CORRELATION_THRESHOLD), out_analyze(data, OUTLIER_THRESHOLD))

def get_missing_diag(data):
    return format_missing_diag(check_missing(over_analyze(data)), True)

def get_corr_diag(data):
    return format_corr_diag(check_correlation(corr_analyze(data, CORRELATION_THRESHOLD)), True)

def get_outliers_diag(data):
    return format_outliers_diag(check_outliers(out_analyze(data, OUTLIER_THRESHOLD)), True)

def get_distribution_diag(data):
    return format_distribution_diag(check_distribution(data), True)

def get_diagnostics(data):
    missing = check_missing(over_analyze(data))
    corr = check_correlation(corr_analyze(data, CORRELATION_THRESHOLD))
    outliers = check_outliers(out_analyze(data, OUTLIER_THRESHOLD))
    distribution = check_distribution(data)

    return format_diagnostics(missing, corr, outliers, distribution)