from fitlater.advisory.outliers import handle_outliers

def test_high_outliers():
    data = {'outlier_percentage': 40}
    result = handle_outliers('A', data, {})

    assert result['priority'] == 1

def test_zero_outliers():
    data = {'outlier_percentage': 0}
    result = handle_outliers('A', data, {})

    assert result['priority'] == 3