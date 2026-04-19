from fitlater.pipeline import get_diagnostics, get_advisory_report
import pandas as pd

def get_result(data:pd.DataFrame) -> dict:

    if data.empty:
        return {
            "diagnostics": {
                "missing": {"percentage": 0, "columns": 0},
                "distribution": {"max_skew": 0},
                "outliers": {"percentage": 0, "columns": 0},
                "correlation": {"max_corr": 0}
            },
            "advisory": {
                "high": [],
                "medium": [],
                "low": []
            },
            "meta": {
                "rows": 0,
                "columns": 0
            }
        }
    
    diagnostics = get_diagnostics(data, True)
    advisory = get_advisory_report(data, True)

    diagnostics = format_diagnostics(diagnostics)
    advisory = format_advisory(advisory)

    diagnostics = {
        'missing':diagnostics.get('missing',{}),
        'distribution':diagnostics.get('distribution',{}),
        'outliers':diagnostics.get('outliers',{}),
        'correlation':diagnostics.get('correlation',{})
    }

    return {
        'diagnostics':diagnostics,
        'advisory':advisory,
        'meta':{
            'rows':data.shape[0],
            'columns':data.shape[1]
        }
    }

def format_diagnostics(diagnostics:dict) -> dict:
    
    def get_data(section):
        section_data = diagnostics.get(section, {})
        if "data" not in section_data:
            raise ValueError(f"Invalid diagnostics format: {section}")
        return section_data["data"]

    # Missing
    missing_data = get_data('missing')
    missing_cols = len(missing_data)

    missing_percentage = (
        sum(v['missing_percentage'] for v in missing_data.values()) / missing_cols
        if missing_cols > 0 else 0
    )

    # Outliers
    outlier_data = get_data('outliers')
    outlier_cols = len(outlier_data)
    outlier_percentage = (
        sum(v['outlier_percentage'] for v in outlier_data.values()) / outlier_cols
        if outlier_cols > 0 else 0
    )

    # Distribution
    skew_data = get_data('distribution')
    max_skew = max(
        [v['skew'] for v in skew_data.values()],
        default=0
    )

    # Correlation
    corr_pairs = get_data('correlation')
    max_corr = max(
        [abs(v['correlation']) for v in corr_pairs.values()],
        default=0
    )

    return {
        'missing':{
            'percentage': round(missing_percentage, 2),
            'columns':missing_cols
        },
        'distribution':{
            'max_skew':round(max_skew, 4)
        },
        'outliers':{
            'percentage':round(outlier_percentage, 2),
            'columns':outlier_cols
        },
        'correlation':{
            'max_corr':round(max_corr, 4)
        }
    }

def format_advisory(advisory):

    advisory = advisory or []  # handle None safely

    def extract(priority_level):
        return [
            {
                "column": x.get("column"),
                "recommendation": x.get("recommendation"),
                "reason": x.get("reason")
            }
            for x in advisory
            if isinstance(x, dict) and x.get("priority") == priority_level
        ]

    return {
        "high": extract(1),
        "medium": extract(2),
        "low": extract(3)
    }