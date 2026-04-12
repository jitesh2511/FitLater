from fitlater.cli.formatter.base import _heading, _section

from fitlater.config import PRIORITY_LABELS, ISSUE_LABELS

def _format_single(advice: dict) -> str:

    return f"""
    Column: {advice['column']}
    → Issue: {ISSUE_LABELS[advice['issue']]}
    → Recommendation: {advice['recommendation']}
    → Reason: {advice['reason']} 
    """.strip()

def format_advice(advice_list: list) -> str:

    heading = _heading('ADVISORY REPORT')

    def build_section(title, items):
        if not items:
            return ""
        return _section(title) + '\n'.join(items)

    high = [_format_single(a) for a in advice_list if a['priority'] == 1]
    medium = [_format_single(a) for a in advice_list if a['priority'] == 2]
    low = [_format_single(a) for a in advice_list if a['priority'] == 3]

    sections = [
        heading,
        build_section(f'HIGH PRIORITY (showing {min(len(high), 10)} out of {len(high)})', high[:10]),
        build_section(f'MEDIUM PRIORITY (showing {min(len(medium), 10)} out of {len(medium)})', medium[:10]),
        build_section(f'LOW PRIORITY (showing {min(len(low), 10)} out of {len(low)})', low[:10])
    ]

    return '\n\n'.join(filter(None, sections))
    
    