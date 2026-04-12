from fitlater.advisory.correlation import handle_corr

def test_high_corr():
    data = {
        'feature_1': 'A',
        'feature_2': 'B',
        'correlation': 0.95
    }

    result = handle_corr(data, {}, {})

    assert result['priority'] == 1

def test_low_corr():
    data = {
        'feature_1': 'A',
        'feature_2': 'B',
        'correlation': 0.2
    }

    result = handle_corr(data, {}, {})

    assert result['priority'] == -1

