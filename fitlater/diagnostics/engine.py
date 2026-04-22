'''

This is the engine module for Diagnostics Layer. It acts as the main orchestrator for
the layer and calls required functions to generate a list of diagnostics on the given set.

The engine uses computated values from descriptive layer as well as computes required values
from the raw dataset whenever required in order to fulfill it's purpose.

'''

import pandas as pd

from fitlater.diagnostics.constant_column import check_constant
from fitlater.diagnostics.duplicates import check_duplicates
from fitlater.diagnostics.imbalance import check_imbalance
from fitlater.diagnostics.missing import check_missing
from fitlater.diagnostics.outliers import check_outliers
from fitlater.diagnostics.distribution import check_distribution
from fitlater.diagnostics.correlation import check_correlation_all
from fitlater.diagnostics.type_issues import check_type_issues

def build_diagnostics(profile:dict, df:pd.DataFrame) -> list:

    diagnostics = []

    COLUMN_CHECKS = [
        check_missing,
        check_outliers,
        check_distribution,
        check_type_issues,
        check_constant,
        check_imbalance
    ]

    DATASET_CHECKS = [
        check_correlation_all,
        check_duplicates
    ]

    # Column checks
    for col in df.columns:

        for func in COLUMN_CHECKS:
            try:   
                issue = func(col, profile[col], df[col])
                if issue:
                    diagnostics.append(issue)
            except Exception:
                continue

    # Dataset checks
    for func in DATASET_CHECKS:

        try:
            result = func(profile, df)

            if isinstance(result, list):
                diagnostics.extend(result)
            elif result:
                diagnostics.append(result)
        except Exception:
            continue


    return diagnostics