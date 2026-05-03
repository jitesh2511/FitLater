"""
Descriptive contract builder.

Defines `build_contract()` which standardizes the structure returned by
the descriptive layer: dataset `meta`, per-column `profile`, and the
`column_types` mapping. Supports returning an empty contract for
empty datasets.
"""

from copy import deepcopy

def build_contract(dataset_meta:dict, profile:dict, column_types:dict, empty=False) -> dict:

    if empty:
        return {
            'meta': {
                'n_rows': 0,
                'n_cols': 0,
                'memory': ""
            },
            'profile': {

            },
            'column_types':{
                
            }
        }
    
    return {
        'meta': deepcopy(dataset_meta),
        'profile': deepcopy(profile),
        'column_types': deepcopy(column_types)
    }