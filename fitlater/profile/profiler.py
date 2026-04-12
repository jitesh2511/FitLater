import pandas as pd
from fitlater.profile.column import build_column_profile

def get_profile(data: pd.DataFrame):

    profile = {}

    for col in data.columns:
        profile[col] = build_column_profile(data[col])
    
    return profile