'''
This module provides helper functions for diagnostics layer
'''

def make_issue(type:str, column:str, data:dict, severity:str, has_issue:bool) -> dict:
    return {
        'type': type,
        'column': column,
        'data': data,
        'meta': {
            'has_issue': has_issue,
            'severity': severity
        }
    }

severity_order = {
        'low': 0,
        'medium': 1,
        'high': 2
    }

def get_severity(value:int or float, thresholds:dict) -> str:

    if value <= thresholds['low']:
        return 'low'
    elif value <= thresholds['medium']:
        return 'medium'
    return 'high'