def build_advice(column, issue, action, reason, priority):
    return {
        'column': column,
        'issue_type': issue,
        'action': action,
        'reason': reason,
        'priority': priority
    }
