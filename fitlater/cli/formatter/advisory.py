from fitlater.cli.formatter.base import _heading, _section
from fitlater.config import ISSUE_LABELS


def _format_single(advice: dict) -> str:
    return (
        f"Column: {advice['column']}\n"
        f"→ Issue: {ISSUE_LABELS.get(advice['issue_type'], advice['issue_type'])}\n"
        f"→ Recommendation: {advice['action']}\n"
        f"→ Reason: {advice['reason']}"
    )


def format_advice(advice_list: list, args) -> str:

    if not advice_list:
        return "\nNo advisory generated.\n"

    if not '--full' in args:
        advice_list = [a for a in advice_list if not a['priority'] == 3]

    heading = _heading("ADVISORY REPORT")

    def build_section(title, items):
        if not items:
            return ""
        return _section(title) + "\n".join(items)

    high = [_format_single(a) for a in advice_list if a["priority"] == 1]
    medium = [_format_single(a) for a in advice_list if a["priority"] == 2]
    low = [_format_single(a) for a in advice_list if a["priority"] == 3]

    sections = [
        heading,
        build_section(f"HIGH PRIORITY ({len(high)})", high[:10]),
        build_section(f"MEDIUM PRIORITY ({len(medium)})", medium[:10]),
        build_section(f"LOW PRIORITY ({len(low)})", low[:10]),
    ]

    return "\n\n".join(filter(None, sections))