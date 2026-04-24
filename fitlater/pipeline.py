from fitlater.core.engine import build_description
from fitlater.diagnostics.engine import build_diagnostics
from fitlater.advisory.engine import get_advice


def run_pipeline(df):

    if df is None or len(df) == 0:
        raise ValueError("Empty dataset provided")

    descriptive = build_description(df)

    profile = descriptive["profile"]

    diagnostics = build_diagnostics(profile, df)

    advisory = get_advice(profile, diagnostics)

    return {
        "descriptive": descriptive,
        "diagnostics": diagnostics,
        "advisory": advisory
    }