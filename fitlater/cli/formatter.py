import os
from fitlater.config import (
    NAME,
    VERSION,
    MISSING_THRESHOLD,
    SKEW_THRESHOLD,
    HIGH_CARDINALITY_THRESHOLD,
    DUPLICATE_THRESHOLD,
)

# Safe terminal width
try:
    WIDTH = os.get_terminal_size().columns
except OSError:
    WIDTH = 100


def _heading(title: str) -> str:
    return f"\n{title.center(WIDTH, '=')}\n"


def _section(title: str) -> str:
    line = "-" * len(title)
    return f"\n{line}\n{title}\n{line}\n"

def info() -> str:
    lines = []
    start = "\033[1m"
    end = "\033[0m"
    lines.append(f'\n\n{start}{NAME}')
    lines.append(f'v{VERSION}{end}')

    return '\n'.join(lines) + '\n'

def _format_overview(result: dict) -> str:
    if not result:
        return "\nNo data available.\n"

    lines = []
    lines.append(_heading("Overview"))

    # ---------------- SHAPE ----------------
    shape = result.get("shape", {})
    lines.append(_section("Dataset Shape"))
    lines.append(f"Rows: {shape.get('n_rows', 0)}")
    lines.append(f"Columns: {shape.get('n_cols', 0)}")
    lines.append(f"Memory Usage: {shape.get('memory_usage', 0)} MB")

    # ------------- COLUMN TYPES -------------
    classification = result.get("column_classification", {})
    lines.append(_section("Column Types"))
    lines.append(f"Numerical: {len(classification.get('numerical', []))}")
    lines.append(f"Categorical: {len(classification.get('categorical', []))}")
    lines.append(f"Boolean: {len(classification.get('boolean', []))}")
    lines.append(f"Others: {len(classification.get('others', []))}")

    # ------------- MISSING -------------
    missing = result.get("missing", {})
    lines.append(_section("Missing Values"))
    total_missing = missing.get("total_missing", 0)
    lines.append(f"Total Missing Values: {total_missing}")

    high_missing_cols = []
    for col, pct in missing.get("missing_percentage", {}).items():
        if pct >= MISSING_THRESHOLD:
            high_missing_cols.append((col, pct))

    if high_missing_cols:
        lines.append(f"\nColumns with > {MISSING_THRESHOLD}% missing:")
        for col, pct in high_missing_cols:
            lines.append(f"- {col} ({pct:.2f}%)")
    else:
        lines.append("\nNo columns exceed missing threshold.")

    # ------------- SKEW -------------
    numerical_summary = result.get("numerical_summary", {})
    skewed = []

    for col, metrics in numerical_summary.items():
        skew_val = metrics.get("skew")
        if skew_val is not None and abs(skew_val) >= SKEW_THRESHOLD:
            skewed.append((col, skew_val))

    lines.append(_section("Skewed Numerical Features"))

    if skewed:
        for col, skew_val in skewed:
            lines.append(f"- {col} (skew = {skew_val:.2f})")
    else:
        lines.append("No highly skewed numerical features detected.")

    # ------------- HIGH CARDINALITY -------------
    categorical_summary = result.get("categorical_summary", {})
    high_card = []

    for col, info in categorical_summary.items():
        if info.get("n_unique", 0) >= HIGH_CARDINALITY_THRESHOLD:
            high_card.append((col, info.get("n_unique")))

    lines.append(_section("High Cardinality Categorical Features"))

    if high_card:
        for col, count in high_card:
            lines.append(f"- {col} ({count} unique values)")
    else:
        lines.append("No high-cardinality categorical columns detected.")

    # ------------- DUPLICATES -------------
    duplicates = result.get("duplicates", {})
    dup_count = duplicates.get("n_dup", 0)
    dup_pct = duplicates.get("dup_per", 0)

    lines.append(_section("Duplicates"))
    lines.append(f"Duplicate Rows: {dup_count} ({dup_pct:.2f}%)")

    if dup_pct >= DUPLICATE_THRESHOLD:
        lines.append("⚠ Duplicate percentage exceeds threshold.")

    return "\n".join(lines) + "\n"