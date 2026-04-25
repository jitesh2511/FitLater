from fitlater.cli.formatter.base import _heading, _section


def format_descriptive(descriptive: dict) -> str:

    if not descriptive:
        return "\nNo descriptive data available.\n"

    meta = descriptive.get("meta", {})
    profile = descriptive.get("profile", {})

    lines = []
    lines.append(_heading("DESCRIPTIVE SUMMARY"))

    # ---------------- DATASET INFO ----------------
    lines.append(_section("Dataset Info"))
    lines.append(f"Rows: {meta.get('n_rows', 0)}")
    lines.append(f"Columns: {meta.get('n_cols', 0)}")

    # ---------------- COLUMN TYPE SUMMARY (DERIVED) ----------------
    lines.append(_section("Column Type Summary"))

    type_counts = {}

    for col, stats in profile.items():
        col_type = stats.get("type", "unknown")
        type_counts[col_type] = type_counts.get(col_type, 0) + 1

    if type_counts:
        for t, count in type_counts.items():
            lines.append(f"{t.capitalize()}: {count}")
    else:
        lines.append("No column type information available.")

    # ---------------- SAMPLE COLUMN PREVIEW ----------------
    lines.append(_section("Sample Column Overview"))

    for i, (col, stats) in enumerate(profile.items()):
        col_type = stats.get("type", "unknown")
        lines.append(f"{col} → {col_type}")

        if i >= 4:  # show only 5 columns
            break

    return "\n".join(lines) + "\n"