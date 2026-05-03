"""
Small utility helpers for building advisory payloads.

Exports `build_advice()` which standardizes the structure returned by
advisory handlers: a dictionary containing the `column`, `issue_type`,
recommended `action`, `reason`, and numeric `priority`.
"""

def build_advice(column, issue, action, reason, priority):
    return {
        'column': column,
        'issue_type': issue,
        'action': action,
        'reason': reason,
        'priority': priority
    }
