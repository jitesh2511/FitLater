def make_issue(type, data, has_Issue, max_severity):
    return {
        'type': type,
        'data': data,
        'meta' : {
            'has_issue': has_Issue,
            'max_severity': max_severity
        }
    }

severity_order = {
        'low': 0,
        'medium': 1,
        'high': 2
    }

def get_max_severity(data):
    severities = [v["severity"] for v in data.values()]

    if severities:
        max_sev = max(severities, key=lambda x: severity_order[x])
    else:
        max_sev = "low"
    
    return max_sev
