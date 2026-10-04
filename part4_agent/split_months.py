"""
Helper script -- splits Part 1's monthly_category_revenue.csv into one
flat CSV per month, so mock_agent_runner.run() has a "previous month" and
"current month" feed to compare, the same shape a real monthly ingestion
would hand the agent.

Run this once after Part 1 (and any time Part 1's output changes):
    python split_months.py
"""

import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "..", "part1_sql", "output", "monthly_category_revenue.csv")

MONTHS = ["April", "May", "June"]


def main():
    rows = list(csv.DictReader(open(SOURCE)))

    for month in MONTHS:
        month_rows = [r for r in rows if r["month"] == month]
        out_path = os.path.join(BASE, f"{month.lower()}_revenue.csv")
        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["month", "category", "revenue", "n_orders"])
            writer.writeheader()
            writer.writerows(month_rows)
        print(f"wrote {month} -> {out_path} ({len(month_rows)} rows)")


if __name__ == "__main__":
    main()
