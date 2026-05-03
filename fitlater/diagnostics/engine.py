"""
Diagnostics layer orchestrator.

`build_diagnostics(profile, df)` runs a set of column-level and dataset-level
checks using the diagnostics modules and returns a list of standardized
diagnostic payloads. The engine respects configuration excludes and
gracefully continues on individual check errors.
"""

import pandas as pd

from fitlater.config import DEFAULT_CONFIG

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
        ("missing", check_missing),
        ("outliers", check_outliers),
        ("distribution", check_distribution),
        ("type_issues", check_type_issues),
        ("constant", check_constant),
        ("imbalance", check_imbalance)
    ]

    DATASET_CHECKS = [
        ("correlation", check_correlation_all),
        ("duplicates", check_duplicates)
    ]

    exclude = DEFAULT_CONFIG['diagnostics']['exclude']

    # Column checks
    for col in df.columns:

        for check_type, func in COLUMN_CHECKS:

            if check_type in exclude:
                continue

            try:   
                issue = func(col, profile[col], df[col])
                if issue:
                    diagnostics.append(issue)
            except Exception:
                continue

    # Dataset checks
    for check_type, func in DATASET_CHECKS:

        if check_type in exclude:
            continue

        try:
            result = func(profile, df)

            if isinstance(result, list):
                diagnostics.extend(result)
            elif result:
                diagnostics.append(result)
        except Exception:
            continue


    return diagnostics