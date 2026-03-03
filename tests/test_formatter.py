import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitlater.cli.formatter import (_format_overview, info)
from fitlater.core.overview import analyze

import pandas as pd
import numpy as np

def _data():
    np.random.seed(42)

    df = pd.DataFrame({
        # Numerical column (normal distribution)
        "age": np.random.normal(30, 5, 100),

        # Numerical column with skew
        "income": np.random.exponential(scale=50000, size=100),

        # Numerical column with missing values
        "score": np.append(np.random.randint(50, 100, 95), [np.nan]*5),

        # Boolean column
        "is_student": np.random.choice([True, False], 100),

        # Categorical column
        "city": np.random.choice(["Delhi", "Mumbai", "Chennai"], 100),

        # Categorical with missing
        "department": np.append(
            np.random.choice(["HR", "Tech", "Sales"], 95),
            [np.nan]*5
        ),

        # Datetime column (should go to 'others')
        "join_date": pd.date_range(start="2023-01-01", periods=100, freq="D")
    })

    # Add duplicate rows intentionally
    df = pd.concat([df, df.iloc[:3]], ignore_index=True)

    return df

print(info())
print(_format_overview(analyze(_data())))