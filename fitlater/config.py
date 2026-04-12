# Metadata
NAME = 'FitLater'
VERSION = '0.3.0'

# Correlation 
CORRELATION_THRESHOLD = 0.6

# Outliers
OUTLIER_THRESHOLD = 0.01

# CLI
MISSING_THRESHOLD = 5.0
SKEW_THRESHOLD = 0.5
HIGH_CARDINALITY_THRESHOLD = 50
DUPLICATE_THRESHOLD = 1

# Diagnostics
MISSING_SEVERITY_THRESHOLD = {
    'low': 15,
    'medium': 30,
}

OUTLIER_SEVERITY_THRESHOLD = {
    'low': 15,
    'medium': 30,
}

CORR_SEVERITY_THRESHOLD = {
    'low': 0.7,
    'medium' : 0.85
}

SKEW_SEVERITY_THRESHOLD = {
    'low' : 1.0,
    'medium' : 1.5
}


# Advisory

PRIORITY_LABELS = {
    1: 'HIGH',
    2: 'MEDIUM',
    3: 'LOW'
}

ISSUE_LABELS = {
    'missing': 'Missing Values',
    'outliers': 'Outliers',
    'distribution': 'Distribution',
    'correlation': 'Correlation'
}