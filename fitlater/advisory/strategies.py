def get_imputation_strategy(data) -> str:

    if not data.get('is_numeric'):
        return 'mode'

    skew = data.get('skew')

    if skew is None:
        return 'median'

    if abs(skew) > 1:
        return 'median'
    
    return 'mean'

def get_transformation_strategy(data):

    skew = data.get('skew')

    if skew is None:
        return None
    
    skew = abs(skew)

    if skew > 1:
        return 'log transformation'
    
    if skew > 0.5:
        return 'consider transformation'

    return None