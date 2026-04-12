from fitlater.advisory.correlation import handle_corr
from fitlater.advisory.distribution import handle_distribution
from fitlater.advisory.missing import handle_missing
from fitlater.advisory.outliers import handle_outliers

def get_advice(profile:dict, diagnostics:list):
    results = []

    for diag in diagnostics:

        if diag['type'] == 'missing' and diag['meta']['has_issue']:

            for column, data in diag['data'].items():
                advice = handle_missing(column, data, profile[column])
                results.append(advice)
        
        elif diag['type'] == 'outliers' and diag['meta']['has_issue']:

            for column, data in diag['data'].items():
                advice = handle_outliers(column, data, profile[column])
                results.append(advice)
        
        elif diag['type'] == 'distribution' and diag['meta']['has_issue']:

            for column, data in diag['data'].items():
                advice = handle_distribution(column, data, profile[column])
                if advice['priority'] > 0:
                    results.append(advice)
        
        elif diag['type'] == 'correlation' and diag['meta']['has_issue']:

            for _, data in diag['data'].items():
                advice = handle_corr(data, profile[data['feature_1']], profile[data['feature_2']])
                if advice['priority'] > 0:
                    results.append(advice)


    results.sort(key=lambda x: x['priority'])

    return results