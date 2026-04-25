from fitlater.pipeline import run_pipeline
import pandas as pd


def get_result(df: pd.DataFrame) -> dict:

    if df.empty:
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

    result = run_pipeline(df)

    descriptive = result["descriptive"]
    diagnostics = result["diagnostics"]
    advisory = result["advisory"]   # already includes ALL priorities

    return {
        "diagnostics": format_diagnostics_ui(diagnostics),
        "advisory": format_advisory_ui(advisory),
        "meta": {
            "rows": descriptive["meta"]["n_rows"],
            "columns": descriptive["meta"]["n_cols"]
        }
    }


# -------------------------------
# UI FORMATTERS (Adapter Layer)
# -------------------------------

def format_diagnostics_ui(diagnostics: list) -> dict:

    missing_cols = 0
    missing_total = 0

    outlier_cols = 0
    outlier_total = 0

    max_skew = 0
    max_corr = 0

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

        elif issue == "correlation":
            corr = abs(details.get("correlation", 0))
            max_corr = max(max_corr, corr)

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
        "correlation": {
            "max_corr": round(max_corr, 4)
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