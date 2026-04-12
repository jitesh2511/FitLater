from fitlater.advisory.distribution import handle_distribution

def test_high_skew():
    data = {'skew': 2}
    profile = {'skew': 2}

    result = handle_distribution('A', data, profile)

    assert result['priority'] == 1

def test_no_skew():
    data = {'skew': 0.1}
    profile = {'skew': 0.1}

    result = handle_distribution('A', data, profile)

    assert result['priority'] == -1