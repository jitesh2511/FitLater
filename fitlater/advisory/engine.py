from fitlater.advisory.constant_column import handle_constant
from fitlater.advisory.correlation import handle_corr
from fitlater.advisory.distribution import handle_distribution
from fitlater.advisory.duplicates import handle_duplicates
from fitlater.advisory.imbalance import handle_imbalance
from fitlater.advisory.missing import handle_missing
from fitlater.advisory.outliers import handle_outliers
from fitlater.advisory.type_issues import handle_type_issue

HANDLERS = {
    'missing': handle_missing,
    'outliers': handle_outliers,
    'distribution': handle_distribution,
    'corr': handle_corr,
    'type_issue': handle_type_issue,
    'constant': handle_constant,
    'imbalance': handle_imbalance,
    'duplicates': handle_duplicates
}

def get_advice(profile:dict, diagnostics:list):
    results = []

    for diag in diagnostics:

        if not diag['meta']['has_issue']:
            continue

        issue_type = diag['type']

        handler = HANDLERS.get(issue_type)

        if handler:
            advice = handler(profile, diag)
            if advice and advice['priority'] > 0:
                results.append(advice)


    results.sort(key=lambda x: x['priority'])

    return results