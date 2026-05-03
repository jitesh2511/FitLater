"""
Advisory helpers for dataset duplicate detection.

Contains logic to produce recommendations when duplicate rows are
identified in a dataset. It evaluates the duplicate percentage and
returns suggested actions (e.g., remove duplicates) with reasons and
priority levels to be consumed by the advisory engine.
"""

from fitlater.advisory.util import build_advice

def handle_duplicates(profile:dict, diag:dict) -> dict | None:

    data = diag["data"]
    severity = diag.get("meta", {}).get("severity")

    dup_pct = data["details"]["duplicate_pct"]

    if severity == "high":
        action = "Remove duplicate rows immediately"
        reason = f"High duplicate percentage ({dup_pct}%) can bias model training"
        priority = 1

    elif severity == "medium":
        action = "Consider removing duplicate rows"
        reason = f"Moderate duplicate percentage ({dup_pct}%) may affect results"
        priority = 2

    else:
        action = "No immediate action required"
        reason = f"Low duplicate percentage ({dup_pct}%) is unlikely to affect results"
        priority = 3

    return build_advice("dataset", "duplicates", action, reason, priority)