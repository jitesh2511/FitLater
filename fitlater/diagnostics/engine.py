'''

This is the engine module for Diagnostics Layer. It acts as the main orchestrator for
the layer and calls required functions to generate a list of diagnostics on the given set.

The engine uses computated values from descriptive layer as well as computes required values
from the raw dataset whenever required in order to fulfill it's purpose.

'''

from numpy import diag
import pandas as pd

from fitlater.diagnostics import distribution
from fitlater.diagnostics.missing import check_missing
from fitlater.diagnostics.outliers import check_outliers
from fitlater.diagnostics.distribution import check_distribution
from fitlater.diagnostics.correlation import check_correlation_all

def build_diagnostics(profile:dict, df:pd.DataFrame) -> list:

    diagnostics = []

    for col in df.columns:

        # Build missing diagnostics
        missing = check_missing(col, profile[col])
        if missing:
            diagnostics.append(missing)

        # Build outlier diagnostics
        outliers = check_outliers(col, profile[col], df[col])
        if outliers:
            diagnostics.append(outliers)

        # Build distribution diagnostics
        distribution = check_distribution(col, profile[col])
        if distribution:
            diagnostics.append(distribution)

    # Build correlation diagnostics
    corr_diags = check_correlation_all(profile, df)
    if corr_diags:
        diagnostics.extend(corr_diags)


    return diagnostics