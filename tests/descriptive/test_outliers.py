from fitlater.core.outliers import analyze_outliers
import pandas as pd
import numpy as np

def create_sample_df():

    np.random.seed(42)

    df = pd.DataFrame({
        # Normal distribution (should have few/no outliers)
        "normal_dist": np.random.normal(loc=50, scale=5, size=100),

        # Strong outliers added manually
        "with_outliers": np.concatenate([
            np.random.normal(100, 10, 95),
            np.array([200, 220, 250, 300, 350])  # extreme values
        ]),

        # Uniform distribution (unlikely strong outliers)
        "uniform_dist": np.random.uniform(0, 1, 100),

        # Constant column (edge case)
        "constant_col": np.ones(100) * 10,

        # Small variance column
        "small_variance": np.random.normal(0, 0.01, 100),

        # Negative values with extreme negative outlier
        "negative_values": np.concatenate([
            np.random.normal(-20, 5, 98),
            np.array([-100, -120])
        ]),

        # Categorical column (should be ignored by outlier module)
        "category": np.random.choice(["A", "B", "C"], 100)
    })
    return df

def test_outlier_structure():

    result = analyze_outliers(create_sample_df(), 0.01)

    expected_keys = {
        'method',
        'outlier_counts',
        'outlier_percentage',
        'columns_with_outliers',
        'bounds',
        'outlier_summary',
    }

    assert set(result.keys()) == expected_keys
    # bounds is {column_name: {lower_bound, upper_bound}} per numeric feature
    for col, b in result['bounds'].items():
        assert set(b.keys()) == {'lower_bound', 'upper_bound'}
    assert set(result['outlier_summary'].keys()) == {
        'n_numeric_features',
        'n_features_with_outliers',
        'max_outlier_percentage',
    }


def test_outlier_values():
    result = analyze_outliers(create_sample_df(), 0.01)

    assert result['method'] == 'IQR'
    assert result['outlier_counts']['with_outliers'] >= 5
    assert result['outlier_counts']['constant_col'] == 0
    assert 'category' not in result['outlier_counts']
    assert 'with_outliers' in result['columns_with_outliers']
    assert result['outlier_summary']['n_numeric_features'] == 6
