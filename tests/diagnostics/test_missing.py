from fitlater.diagnostics.missing import check_missing
from fitlater.core.overview import analyze


import pytest
import pandas as pd
import numpy as np

def create_missing_df():
    np.random.seed(42)
    df = pd.DataFrame({
        # Standard case: Some missing, some present
        "A": [1, 2, np.nan, 4, 5],
        # Multiple missing at start, no missing at end
        "B": [np.nan, np.nan, 3, 4, 5],
        # No missing values at all
        "C": [1, 2, 3, 4, 5],
        # All values missing
        "D": [np.nan, np.nan, np.nan, np.nan, np.nan],
        # Single missing (as None) in object dtype (string)
        "E": ["a", None, "c", "d", "e"],
        # All values are None (object column)
        "F": [None, None, None, None, None],
        # Some boolean values (no missing)
        "G": [True, False, True, False, True],
        # All missing via np.nan for float
        "H": [np.nan] * 5,
        # Mixture of different NA values (None, np.nan, pd.NA)
        "I": [None, np.nan, pd.NA, 1, 2],
        # Row with a NaN in integer array (will be float)
        "J": [1, 2, np.nan, 4, 5],
        # All 0, no missing
        "K": [0, 0, 0, 0, 0],
        # Single value, all others missing
        "L": [None, None, 'x', None, None],
        # Category dtype with missing
        "M": pd.Series(['red', None, 'blue', 'red', None], dtype='category')
    })
    return check_missing(analyze(df))

def test_missing_structure():

    missing = create_missing_df()

    expected_keys = {'type','data','meta'}
    meta_keys = {'has_issue', 'max_severity'}

    assert set(missing.keys()) == expected_keys
    assert set(missing['meta'].keys())  == meta_keys

def test_missing_values():

    missing = create_missing_df()
    
    # Test global properties
    assert missing['type'] == 'missing'
    assert isinstance(missing['data'], dict)
    assert isinstance(missing['meta'], dict)
    assert missing['meta']['has_issue'] is True
    assert missing['meta']['max_severity'] == 'high'

    # Test all columns in the test dataframe
    expected = {
        'A': (20.0, 'medium'),
        'B': (40.0, 'high'),
        'C': (0.0, 'low'),
        'D': (100.0, 'high'),
        'E': (20.0, 'medium'),
        'F': (100.0, 'high'),
        'G': (0.0, 'low'),
        'H': (100.0, 'high'),
        'I': (60.0, 'high'),
        'J': (20.0, 'medium'),
        'K': (0.0, 'low'),
        'L': (80.0, 'high'),
        'M': (40.0, 'high')
    }

    for col, (pct, sev) in expected.items():

        no_missing = ['C', 'G', 'K']

        if col in no_missing:
            assert col not in missing['data']
            continue
        
        assert col in missing['data']
        actual_pct = missing['data'][col]['missing_percentage']
        actual_sev = missing['data'][col]['severity']
        
        # Allow float equality for missing percentage
        assert abs(actual_pct - pct) < 0.01, f"Column {col}: got {actual_pct}, expected {pct}"
        assert actual_sev == sev, f"Column {col}: got {actual_sev}, expected {sev}"

@pytest.mark.parametrize("bad_input", [None, 123, "string", [], {}])
def test_invalid_input(bad_input):
    with pytest.raises(Exception):
        check_missing(analyze(bad_input))

def test_empty_dataframe():
    df = pd.DataFrame()
    result = check_missing(analyze(df))

    assert result['meta']['has_issue'] is False

def test_empty_df_missing():
    df = pd.DataFrame()
    result = check_missing(analyze(df))

    assert result['meta']['has_issue'] is False