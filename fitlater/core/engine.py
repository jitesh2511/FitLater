'''
This module is the orchestrator for Descriptive Layer.
It takes the dataset, passes it to required functions,
and builds a descriptive contract.
'''

import pandas as pd

from fitlater.core import visualization
from fitlater.core.contract import build_contract
from fitlater.core.base import get_metadata, get_missing
from fitlater.core.schema import infer_column_types
from fitlater.core.numeric import get_numeric_stats
from fitlater.core.categorical import get_categorical_stats
from fitlater.core.others import get_datetime_stats, get_boolean_stats, get_mixed_stats
from fitlater.core.visualization import (
    getHistogramData,
    getBoxPlotData,
    getBarChartData,
    getPieChartData,
    getBooleanChartData,
    getTimeSeriesData,
    getBooleanPieChartData,
    getDatetimeWeekdayDistribution
)

def build_description(df:pd.DataFrame) -> dict:

    if df.empty:
        return build_contract(dataset_meta={}, profile={}, column_types= {}, empty=True)
    
    # Meta
    meta = get_metadata(df)

    # Determing dtype of each column
    column_types = infer_column_types(df)

    # Building each column's profile
    profile = {}

    for col, dtype in column_types.items():
    
        series = df[col]

        if dtype == 'numeric':
            stats = get_numeric_stats(series)

            visualizations = {
                "primary": getHistogramData(series),
                "secondary": getBoxPlotData(series)
            }

        elif dtype == 'boolean':
            stats = get_boolean_stats(series)

            visualizations = {
                "primary": getBooleanChartData(series),
                "secondary": getBooleanPieChartData(series)
            }

        elif dtype == 'categorical':
            stats = get_categorical_stats(series)

            visualizations = {
                "primary": getBarChartData(series),
                "secondary": getPieChartData(series)
            }

        elif dtype == 'identifier':
            stats = get_categorical_stats(series)

            visualizations = {
                "primary": None,
                "secondary": None
            }

        elif dtype == 'datetime':
            stats = get_datetime_stats(series)

            visualizations = {
                "primary": getTimeSeriesData(series),
                "secondary": getDatetimeWeekdayDistribution(series)
            }

        elif dtype == 'mixed':
            stats = get_mixed_stats(series)
            visualizations = {
                "primary": None,
                "secondary": None
            }

        else:
            stats = {}
            visualizations = {
                "primary": None,
                "secondary": None
            }

        col_missing = get_missing(series)
        
        profile[col] = {
            'type': dtype,
            **stats,
            **col_missing,
            'visualizations': visualizations
        }
    
    return build_contract(meta, profile, column_types)