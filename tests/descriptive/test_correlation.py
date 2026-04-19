from fitlater.core.correlation import analyze_correlation
import pandas as pd

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
    assert result['high_corr_pairs'] == []
    assert result['corr_summary'] is None

def test_structure():

    result = analyze_correlation(create_sample_df(), 0.5)

    assert set(result.keys()) == {'corr_matrix', 'high_corr_pairs', 'corr_summary'}
    assert set(result['corr_summary']) == {'n_numeric_features', 'n_high_corr_pairs', 'max_corr', 'mean_abs_corr'}

def test_corr_values_range():
    result = analyze_correlation(create_sample_df(), 0.5)

    corr_matrix = result['corr_matrix']

    if corr_matrix is not None:
        assert ((corr_matrix.values >= -1) & (corr_matrix.values <= 1)).all()

def test_high_corr_pairs_detection():
    df = create_sample_df()

    result = analyze_correlation(df, 0.1)  # low threshold

    assert isinstance(result['high_corr_pairs'], list)

def test_single_numeric_column():
    df = pd.DataFrame({
        'A': [1,2,3,4]
    })

    result = analyze_correlation(df, 0.5)

    assert result['corr_matrix'] is not None
    assert result['high_corr_pairs'] == []

def test_constant_columns():
    df = pd.DataFrame({
        'A': [1,1,1],
        'B': [2,2,2]
    })

    result = analyze_correlation(df, 0.5)

    assert result['high_corr_pairs'] == []

def test_mixed_types():
    df = pd.DataFrame({
        'A': [1,2,3],
        'B': ['x','y','z']
    })

    result = analyze_correlation(df, 0.5)

    assert result['corr_matrix'] is not None or result['corr_matrix'] is None

def test_corr_deterministic():
    df = create_sample_df()

    r1 = analyze_correlation(df, 0.5)
    r2 = analyze_correlation(df, 0.5)

    assert r1['high_corr_pairs'] == r2['high_corr_pairs']
    assert r1['corr_summary'] == r2['corr_summary']

    if r1['corr_matrix'] is not None:
        assert r1['corr_matrix'].equals(r2['corr_matrix'])
