from fitlater.advisory.util import build_advice

def handle_corr(data, f1_profile, f2_profile):
    
    f1 = data['feature_1']
    f2 = data['feature_2']
    corr = abs(data['correlation'])

    if corr > 0.9:
        recommendation = 'Drop one of the correlated columns'
        reason = f'Highly correlated features introduce redundancy and multicollinearity. Correlation is {corr}'
        priority = 1
    
    elif corr > 0.7:
        recommendation = 'Consider feature selection or dimensionality reduction'
        reason = f'Moderate correlation may affect the model stability. Correlation is {corr}'
        priority = 2
    else:
        recommendation = 'No action needed'
        reason = f'Correlation is within acceptable range. Correlation is {corr}'
        priority = -1
    
    column = f'{f1} and {f2}'

    return build_advice(column, 'correlation', recommendation, reason, priority)