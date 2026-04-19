from fitlater.advisory.missing import handle_missing

def test_high_missing():
    data = {'missing_percentage': 80}
    profile = {'is_numeric': True, 'skew': 0}

    result = handle_missing('A', data, profile)

    assert result['priority'] == 1
    assert 'Drop column' in result['recommendation']

def test_imputation_strategy():
    data = {'missing_percentage': 10}
    profile = {'is_numeric': True, 'skew': 2}

    result = handle_missing('A', data, profile)

    assert 'median' in result['recommendation']