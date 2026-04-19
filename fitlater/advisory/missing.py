from fitlater.advisory.util import build_advice
from fitlater.advisory.strategies import get_imputation_strategy

def handle_missing(column, data, profile):

    missing_per = data['missing_percentage']

    if missing_per > 50:
        priority = 1
    elif missing_per > 20:
        priority = 2
    else:
        priority = 3


    if priority == 1:
        recommendation = 'Drop column' 
        reason = 'Too many missing values'
    else:
        strategy = get_imputation_strategy(profile)

        if strategy == 'median':
            recommendation = 'Fill with median'
            reason = 'Median is robust to skewed data and outliers'

        elif strategy == 'mode':
            recommendation = 'Fill with mode'
            reason = 'Mode is appropriate for categorical data'

        else:
            recommendation = 'Fill with mean'
            reason = 'Mean is suitable for approximately normally distributed data'

    reason = f'{reason}. Missing percentage is {round(missing_per, 2)}%'
    return build_advice(column, 'missing', recommendation, reason, priority)