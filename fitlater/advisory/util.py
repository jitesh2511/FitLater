def build_advice(column, issue, recommendation, reason, priority):
    return {
        'column': column,
        'issue': issue,
        'recommendation': recommendation,
        'reason': reason,
        'priority': priority
    }
