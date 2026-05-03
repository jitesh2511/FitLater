"""
Configuration and constants.

Centralizes all configuration parameters, thresholds, and constants used
by the descriptive, diagnostic, and advisory engines. Values are sourced
from environment variables where available.
"""

import os
from dotenv import load_dotenv

load_dotenv()

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))
MAX_ROWS = int(os.getenv("MAX_ROWS", 50000))
MAX_COLS = int(os.getenv("MAX_COLS", 100))
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "csv").split(",")
API_BASE_URL = os.getenv("API_BASE_URL")

# Metadata
NAME = 'FitLater'
VERSION = '1.0.0'

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
DATETIME_LIKE_RATIO_THRESHOLD = 0.9

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