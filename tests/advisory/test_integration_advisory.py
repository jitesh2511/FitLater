from fitlater.advisory.engine import get_advice

from fitlater.diagnostics.missing import check_missing
from fitlater.diagnostics.correlation import check_correlation
from fitlater.diagnostics.distribution import check_distribution
from fitlater.diagnostics.outliers import check_outliers

from fitlater.core.overview import analyze
from fitlater.core.correlation import analyze_correlation
from fitlater.core.outliers import analyze_outliers

from fitlater.profile.profiler import get_profile

from fitlater.config import OUTLIER_THRESHOLD, CORRELATION_THRESHOLD

import pandas as pd
import numpy as np

def create_df():
    np.random.seed(42)
    n = 100

    df = pd.DataFrame({

        # 🔴 Missing-heavy column (should trigger HIGH priority)
        "high_missing": [np.nan]*70 + list(np.random.randint(1, 10, 30)),

        # 🟡 Moderate missing (MEDIUM priority)
        "medium_missing": [np.nan]*30 + list(np.random.randint(1, 10, 70)),

        # 🟢 No missing (LOW / ignored)
        "no_missing": np.random.randint(1, 10, n),

        # 🔴 Strong positive skew
        "high_skew": np.random.exponential(scale=2, size=n),

        # 🟡 Mild skew
        "mild_skew": np.concatenate([
            np.random.normal(10, 2, n//2),
            np.random.normal(12, 2, n//2)
        ]),

        # 🟢 Normal distribution (no skew issue)
        "normal_dist": np.random.normal(0, 1, n),

        # 🔴 Outliers heavy
        "high_outliers": np.concatenate([
            np.random.normal(50, 5, 90),
            np.array([200, 220, 250, 300, 350, 400, 450, 500, 550, 600])
        ]),

        # 🟡 Moderate outliers
        "medium_outliers": np.concatenate([
            np.random.normal(100, 10, 95),
            np.array([200, 220, 250, 300, 350])
        ]),

        # 🟢 No outliers (clean)
        "clean_numeric": np.random.normal(10, 2, n),

        # 🔴 Perfect correlation pair
        "corr_1": np.arange(n),
        "corr_2": np.arange(n),  # perfectly correlated

        # 🟡 Moderate correlation
        "corr_3": np.arange(n) + np.random.normal(0, 5, n),

        # 🔵 Non-numeric column (should be ignored in many places)
        "category": ["A", "B", "C", "D"] * 25,

        # 🔵 Boolean column
        "boolean": [True, False] * 50
    })

    return df

def get_missing_diag():
    return check_missing(analyze(create_df()))

def get_profile_diagnostics():
    df = create_df()
 
    missing = get_missing_diag()
    outliers = check_outliers(analyze_outliers(df, OUTLIER_THRESHOLD))
    corr = check_correlation(analyze_correlation(df, CORRELATION_THRESHOLD))
    dist = check_distribution(df)
    
 

    profile = get_profile(df)
    diagnostics = [missing, outliers, corr, dist]

    return profile, diagnostics


def test_full_advisory_pipeline():

    profile, diagnostics = get_profile_diagnostics()

    result = get_advice(profile, diagnostics)

    assert isinstance(result, list)