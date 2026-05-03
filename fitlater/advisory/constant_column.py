
"""
This module provides advisory logic for handling columns in a dataset that are detected
to be constant (i.e., containing only one unique value). Such columns are generally
not useful for predictive modeling, as they do not provide any variability or information
gain. The core function generates advice to drop these columns, with an associated reason
and priority level, intended for use in fitlater's automated data diagnostics.
"""


from fitlater.advisory.util import build_advice

def handle_constant(profile:dict, diag:dict) -> dict:

    column = diag["column"]

    action = "Drop column"
    reason = "Column has only one unique value and provides no predictive power"
    priority = 1

    return build_advice(column, "constant", action, reason, priority)