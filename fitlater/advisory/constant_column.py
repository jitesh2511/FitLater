from fitlater.advisory.util import build_advice

def handle_constant(profile:dict, diag:dict) -> dict:

    column = diag["column"]

    action = "Drop column"
    reason = "Column has only one unique value and provides no predictive power"
    priority = 1

    return build_advice(column, "constant", action, reason, priority)