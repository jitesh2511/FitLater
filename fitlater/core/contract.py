'''
This module contains the descriptive contract
'''

def build_contract(dataset_meta:dict, profile:dict, column_types:dict, empty=False) -> dict:

    if empty:
        return {
            'meta': {
                'n_rows': 0,
                'n_cols': 0,
                'memory': ""
            },
            'profile': {

            }
        }
    
    return {
        'meta': dataset_meta,
        'profile': profile,
        'column_dtypes': column_types
    }