
"""

This module contains the main entry point for running the FitLater EDA processing pipeline.
It exposes functions (such as `get_result`) that receive a pandas DataFrame, process it through
the diagnostics and advisory steps, and return a structured dictionary suitable for API/class usage.

- Core orchestration for FitLater's backend processing workflow
- Used by API endpoints to analyze datasets and return summaries, diagnostics, advisories, etc.

"""


from backend.util import clean_types
from fitlater.logger.logger_instance import logger


def get_result(df) -> dict:
    from fitlater.pipeline import run_pipeline

    logger.info("Starting processing pipeline")

    try:
        if df.empty:
            return {
                "descriptive": {
                    'meta': {
                    'n_rows': 0,
                    'n_cols': 0,
                    'memory': ""
                    },
                    'profile': {

                    },
                    'column_types':{
                        
                    }
                },
                "diagnostics": {
                    "missing": {"percentage": 0, "columns": 0},
                    "distribution": {"max_skew": 0},
                    "outliers": {"percentage": 0, "columns": 0},
                    "duplicates": {"percentage": 0, "columns": 0}
                },
                "col_diagnostics":{

                },
                "advisory": {
                    "high": [],
                    "medium": [],
                    "low": []
                },
                "meta": {
                    "rows": 0,
                    "columns": 0,
                    "column_list": []
                }
            }

        result = run_pipeline(df)

        descriptive = result["descriptive"]
        diagnostics = result["diagnostics"]
        advisory = result["advisory"]  

        logger.info("Pipeline completed")

        response = {
            'descriptive': descriptive,
            "diagnostics": format_diagnostics_ui(diagnostics),
            "col_diagnostics": diagnostics,
            "advisory": format_advisory_ui(advisory),
            "meta": {
                "rows": descriptive["meta"]["n_rows"],
                "columns": descriptive["meta"]["n_cols"],
                "columns_list": list(df.columns)
            }
        }

        return clean_types(response)

    except Exception as e:
        logger.exception('Pipeline failed')
        raise ValueError("Failed to process dataset")

# -------------------------------
# UI FORMATTERS (Adapter Layer)
# -------------------------------

def format_diagnostics_ui(diagnostics: list) -> dict:

    missing_cols = 0
    missing_total = 0

    outlier_cols = 0
    outlier_total = 0

    max_skew = 0
    duplicate_pct = 0

    for d in diagnostics:
        issue = d.get("type")
        details = d.get("data", {}).get("details", {})

        if issue == "missing":
            missing_cols += 1
            missing_total += details.get("missing_pct", 0)

        elif issue == "outliers":
            outlier_cols += 1
            outlier_total += details.get("outlier_pct", 0)

        elif issue == "distribution":
            skew = abs(details.get("skew", 0))
            max_skew = max(max_skew, skew)

        elif issue == "duplicates":
            duplicate_pct = abs(details.get("duplicate_pct", 0))

    return {
        "missing": {
            "percentage": round(missing_total / missing_cols, 2) if missing_cols else 0,
            "columns": missing_cols
        },
        "distribution": {
            "max_skew": round(max_skew, 4)
        },
        "outliers": {
            "percentage": round(outlier_total / outlier_cols, 2) if outlier_cols else 0,
            "columns": outlier_cols
        },
        "duplicates": {
            "percentage": round(duplicate_pct, 2)
        }
    }


def format_advisory_ui(advisory: list) -> dict:

    def extract(priority):
        return [
            {
                "column": a.get("column"),
                "issue": a.get("issue_type"),
                "recommendation": a.get("action"),  # mapped
                "reason": a.get("reason")
            }
            for a in advisory
            if a.get("priority") == priority
        ]

    return {
        "high": extract(1),
        "medium": extract(2),
        "low": extract(3)
    }