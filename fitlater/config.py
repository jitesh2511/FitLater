# Metadata
NAME = 'FitLater'
VERSION = '0.4.0'

# Configurations
DEFAULT_CONFIG = {
    "diagnostics": {
        "include": None,          
        "exclude": {"imbalance"}  
    }
}

# DESCRIPTIVE
IDENTIFIER_THRESHOLD = 0.95
NUMERIC_LIKE_RATIO_THRESHOLD = 0.9

# CLI
MISSING_THRESHOLD = 5.0
SKEW_THRESHOLD = 0.5
HIGH_CARDINALITY_THRESHOLD = 50
DUPLICATE_THRESHOLD = 1

# DIAGNOSTICS

CORRELATION_THRESHOLD = 0.6
OUTLIER_THRESHOLD = 0.01

MISSING_SEVERITY_THRESHOLD = {
    'low': 15,
    'medium': 30
}

OUTLIER_SEVERITY_THRESHOLD = {
    'low': 15,
    'medium': 30
}

CORR_SEVERITY_THRESHOLD = {
    'low': 0.7,
    'medium' : 0.85
}

SKEW_SEVERITY_THRESHOLD = {
    'low' : 1.0,
    'medium' : 1.5
}
IMBALANCE_THRESHOLDS = {
    'low' : 0.65,
    'medium' : 0.9
}
DUPLICATE_THRESHOLD = {
    'low': 10,
    'medium': 20
}

## Type Issues
NUMERIC_RATIO_THRESHOLD = 0.9
DATETIME_RATIO_THRESHOLD = 0.9
MIXED_NUMERIC_THRESHOLD = [0.3, 0.9]
BOOLEAN_SETS = [
    {"yes", "no"},
    {"true", "false"},
    {"0", "1"},
    {"y", "n"},
    {"t", "f"}
]

# ADVISORY

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