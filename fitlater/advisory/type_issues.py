from fitlater.advisory.util import build_advice

def handle_type_issue(profile:dict, diag:dict) -> dict | None:

    column = diag["column"]
    data = diag["data"]

    issue_type = data["issue_type"]

    severity = diag.get("meta", {}).get("severity")

    if severity == "high":
        priority = 1
    elif severity == "medium":
        priority = 2
    else:
        return None

    if issue_type == "numeric_as_string":
        return build_advice(
            column,
            "type_issue",
            "Convert column to numeric",
            "Column contains numeric values stored as strings",
            priority
        )

    elif issue_type == "datetime_as_string":
        return build_advice(
            column,
            "type_issue",
            "Convert column to datetime",
            "Column contains datetime values stored as strings",
            priority
        )

    elif issue_type == "mixed_types":
        return build_advice(
            column,
            "type_issue",
            "Clean inconsistent values",
            "Column contains mixed data types",
            priority
        )

    elif issue_type == "boolean_as_string":
        return build_advice(
            column,
            "type_issue",
            "Convert to boolean",
            "Column contains boolean-like values",
            priority
        )

    return None