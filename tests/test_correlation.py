import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitlater.core.correlation import analyze_correlation
import pandas as pd
import numpy as np
import pytest

def create_sample_df(choice = 1) -> pd.DataFrame:

    if (choice == 1):
        return pd.DataFrame({
            'Location':['Urban','Poor','Poor','Urban','Posh','Rural','Urban','Poor','Urban','Urban'],
            'Rooms':[2,3,1,3,4,2,5,2,1,3],
            'Area':[120,100,90,240,260,100,300,80,120,140],
            'Price':[2300,1500,1200,4300,4200,1450,5000,1150,2200,2500]
        })
    
    if (choice == 2):
        return pd.DataFrame({
            'Name':['Jitesh', 'Bhanuj', 'Asher']
        })

def test_corr_matrix():
    result = analyze_correlation(create_sample_df(), 0.5)

    assert type(result['corr_matrix']) == pd.DataFrame

def test_no_numerical_features():
    result = analyze_correlation(create_sample_df(choice=2), 0.5)

    assert result['corr_matrix'] == None
    assert result['high_correlation_pairs'] == []
    assert result['correlation_summary'] == None

def test_structure():

    result = analyze_correlation(create_sample_df(), 0.5)

    assert set(result.keys()) == {'corr_matrix', 'high_corr_pairs', 'corr_summary'}
    assert set(result['corr_summary']) == {'n_numeric_features', 'n_high_corr_pairs', 'max_corr', 'mean_abs_corr'}