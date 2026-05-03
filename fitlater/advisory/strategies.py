"""
Utility strategies used by advisory rules.

Provides helper strategy functions such as `get_imputation_strategy()` and
`get_transformation_strategy()` used by advisory modules to select sensible
default actions (e.g., whether to use mean/median/mode or apply transformations)
based on column metadata like type and skew.
"""

def get_imputation_strategy(data) -> str:

    if not data.get('type') == 'numeric':
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