from fitlater.core.overview import analyze
import pandas as pd
import numpy as np
import pytest

def create_sample_df():
    return pd.DataFrame({
        'name': ['Jitesh', 'Bhanuj', 'Deepak', 'Jitesh'],
        'marks': [45, np.nan, 67, 45],
        'age': [18, 20, 19, 18],
        'pass': [True, True, False, True],
        'iq': ['average', 'good', 'bad', 'average']
    })

def test_shape():
    df = create_sample_df()
    result = analyze(df)

    assert result['shape']['n_rows'] == 4
    assert result['shape']['n_cols'] == 5

def test_column_classification():
    df = create_sample_df()
    result = analyze(df)


    assert set(result['column_classification']['numerical']) == {'marks','age'}
    assert set(result['column_classification']['boolean']) == {'pass'}
    assert set(result['column_classification']['categorical']) == {'name','iq'}
    assert set(result['column_classification']['others']) == set()

def test_numerical_summary():
    df = create_sample_df()
    result = analyze(df)

    assert result['numerical_summary']['marks']['mean'] == pytest.approx(df['marks'].mean())
    assert result['numerical_summary']['marks']['median'] == pytest.approx(df['marks'].median())
    assert result['numerical_summary']['marks']['std'] == pytest.approx(df['marks'].std())
    assert result['numerical_summary']['marks']['min'] == pytest.approx(df['marks'].min())
    assert result['numerical_summary']['marks']['max'] == pytest.approx(df['marks'].max())
    assert result['numerical_summary']['marks']['skew'] == pytest.approx(df['marks'].skew())
    assert result['numerical_summary']['age']['mean'] == pytest.approx(df['age'].mean())
    assert result['numerical_summary']['age']['median'] == pytest.approx(df['age'].median())
    assert result['numerical_summary']['age']['std'] == pytest.approx(df['age'].std())
    assert result['numerical_summary']['age']['min'] == pytest.approx(df['age'].min())
    assert result['numerical_summary']['age']['max'] == pytest.approx(df['age'].max())
    assert result['numerical_summary']['age']['skew'] == pytest.approx(df['age'].skew())
    
    

def test_categorical_summary():
    df = create_sample_df()
    result = analyze(df)

    assert result['categorical_summary']['name']['n_unique'] == 3
    assert result['categorical_summary']['name']['top_value'] == 'Jitesh'
    assert result['categorical_summary']['name']['top_freq'] == 2
    assert result['categorical_summary']['iq']['n_unique'] == 3
    assert result['categorical_summary']['iq']['top_value'] == 'average'
    assert result['categorical_summary']['iq']['top_freq'] == 2
    

def test_missing_values():
    df = create_sample_df()
    result = analyze(df)

    assert result['missing']['total_missing'] == 1
    assert result['missing']['missing_per_column']['marks'] == 1
    assert result['missing']['missing_percentage']['marks'] == 25

def test_duplicates():
    df = create_sample_df()
    result = analyze(df)

    assert result['duplicates']['n_dup'] == 1

def test_empty_dataframe():
    df = pd.DataFrame()
    result = analyze(df)
    assert result == {}

def test_structure():

    df = create_sample_df()
    result = analyze(df)

    ex_keys = {
        'shape',
        'column_classification',
        'categorical_summary',
        'missing',
        'numerical_summary',
        'duplicates'
    }

    assert set(result.keys()) == ex_keys