from fitlater.advisory.engine import get_advice

from tests.advisory.test_integration_advisory import get_profile_diagnostics, get_missing_diag

profile, diagnostics = get_profile_diagnostics()

def test_engine_structure():
    result = get_advice(profile, diagnostics)

    assert isinstance(result, list)

    for r in result:
        assert set(r.keys()) == {
            'column', 'issue', 'recommendation', 'reason', 'priority'
        }

def test_priority_sorting():
    result = get_advice(profile, diagnostics)

    priorities = [r['priority'] for r in result]
    assert priorities == sorted(priorities)

def test_no_issues():
    diagnostics = [
        {'type': 'missing', 'meta': {'has_issue': False}},
        {'type': 'outliers', 'meta': {'has_issue': False}},
    ]

    result = get_advice({}, diagnostics)

    assert result == []

def test_partial_diagnostics():
    diagnostics = [
        get_missing_diag(),
        {'type': 'outliers', 'meta': {'has_issue': False}}
    ]

    result = get_advice(profile, diagnostics)

    assert len(result) > 0

def test_advisory_deterministic():
    r1 = get_advice(profile, diagnostics)
    r2 = get_advice(profile, diagnostics)

    assert r1 == r2