"""
Part 2 -- Python Guardrail & Growth-Detection Engine.
"""

import csv


def mom_growth(previous: float, current: float) -> float:
    """Month-on-Month growth percentage, rounded to 2 decimals."""
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """
    Returns one of three strings (never a bare boolean):
      "flagged"                 if abs(mom_pct) > threshold
      "not_flagged"             if abs(mom_pct) < threshold
      "escalate_exact_boundary" if abs(mom_pct) == threshold exactly
    """
    magnitude = abs(mom_pct)
    if magnitude == threshold:
        return "escalate_exact_boundary"
    elif magnitude > threshold:
        return "flagged"
    else:
        return "not_flagged"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """
    Input guardrail over a month,category,revenue,n_orders CSV.
    Line numbers are 1-indexed with the header as line 1.
    Returns (True, []) only if there are zero errors.
    """
    errors: list[str] = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            line_num = i + 2
            month = row.get("month", "")
            category = row.get("category", "")
            revenue_raw = row.get("revenue", "")

            if category == "":
                errors.append(f"line {line_num}: missing category (month={month})")
                continue

            if revenue_raw == "":
                errors.append(f"line {line_num}: missing revenue (category={category})")
                continue

            try:
                revenue = float(revenue_raw)
            except ValueError:
                errors.append(f"line {line_num}: revenue not numeric: {revenue_raw!r}")
                continue

            if revenue < 0:
                errors.append(
                    f"line {line_num}: negative revenue ({revenue}) for category={category}"
                )

    return (len(errors) == 0, errors)