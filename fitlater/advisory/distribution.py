from fitlater.advisory.util import build_advice
from fitlater.advisory.strategies import get_transformation_strategy

def handle_distribution(column, data, profile):

    strategy = get_transformation_strategy(profile)
    skew = data.get('skew')

    if strategy == 'log transformation':
        recommendation = 'Apply log or Box-Cox transformation'
        reason = f'Highly skewed data can negatively impact model performance. Skew is {skew}'
        priority = 1
    elif strategy == 'consider transformation':
        recommendation = 'Consider transformation if model is sensitive to distribution'
        reason = f'Moderate skewness may affect some models. Skew is {skew}'
        priority = 2
    else:
        recommendation = 'No action needed'
        reason = f'Data distribution is approximately normal. Skew is {skew}'
        priority = -1
    
    return build_advice(column, 'distribution', recommendation, reason, priority)