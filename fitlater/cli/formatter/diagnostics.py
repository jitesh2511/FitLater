from fitlater.cli.formatter.base import _heading, _section


def _format_single_diag(diag: dict) -> str:

    column = diag["column"]
    issue = diag["type"]
    severity = diag["meta"]["severity"]
    details = diag["data"].get("details", {})

    details_str = ", ".join(f"{k}: {v}" for k, v in details.items())

    return (
        f"Column: {column}\n"
        f"→ Issue: {issue}\n"
        f"→ Severity: {severity}\n"
        f"→ Details: {details_str}"
    )


def format_diagnostics(diagnostics: list, args) -> str:

    if not diagnostics:
        return "\nNo issues detected.\n"

    if not '--full' in args:
        diagnostics = [d for d in diagnostics if not d['meta']['severity'] == 'low']

    heading = _heading("DIAGNOSTICS")

    def build_section(title, items):
        if not items:
            return ""
        return _section(title) + "\n".join(items)

    high = [_format_single_diag(d) for d in diagnostics if d["meta"]["severity"] == "high"]
    medium = [_format_single_diag(d) for d in diagnostics if d["meta"]["severity"] == "medium"]
    low = [_format_single_diag(d) for d in diagnostics if d["meta"]["severity"] == "low"]

    sections = [
        heading,
        build_section(f"HIGH SEVERITY ({len(high)})", high[:10]),
        build_section(f"MEDIUM SEVERITY ({len(medium)})", medium[:10]),
        build_section(f"LOW SEVERITY ({len(low)})", low[:10]),
    ]

    return "\n\n".join(filter(None, sections))