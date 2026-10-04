"""
Part 4 -- Mock Agent Runner.
No network call, no API key, no real message-sending integration.
Drafting and holding for human approval is the entire scope.
"""

import csv
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "part2_engine"))
sys.path.insert(0, os.path.join(BASE, "..", "part3_narrative"))

from growth_engine import mom_growth, is_flagged, validate_feed  # noqa: E402
from template_fill import draft_message  # noqa: E402

TOP_N = 3


def _load_revenue_map(csv_path: str) -> dict:
    revenue_map = {}
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            revenue_map[row["category"]] = float(row["revenue"])
    return revenue_map


def _first_month_label(csv_path: str) -> str:
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            return row["month"]
    return ""


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    # Subtasks 1-2: validate the current feed; Hard Stop if invalid
    valid, errors = validate_feed(current_month_csv)
    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    previous_revenue = _load_revenue_map(previous_month_csv)
    current_revenue = _load_revenue_map(current_month_csv)
    prev_month_label = _first_month_label(previous_month_csv)

    # Subtasks 3-4: mom_growth + is_flagged for every category
    evaluated = []
    for category, curr_rev in current_revenue.items():
        prev_rev = previous_revenue.get(category)
        if prev_rev is None:
            continue
        pct = mom_growth(prev_rev, curr_rev)
        evaluated.append({
            "category": category,
            "mom_pct": pct,
            "previous_revenue": prev_rev,
            "current_revenue": curr_rev,
            "flag": is_flagged(pct),
        })

    # Subtask 7b: exact-boundary categories -> escalated only
    escalated_categories = [e["category"] for e in evaluated
                            if e["flag"] == "escalate_exact_boundary"]

    # Subtask 5: flagged only, sorted by abs(mom_pct) descending
    flagged = [e for e in evaluated if e["flag"] == "flagged"]
    flagged.sort(key=lambda e: abs(e["mom_pct"]), reverse=True)

    # Subtask 6: draft at most the top 3
    to_draft = flagged[:TOP_N]
    to_suppress = flagged[TOP_N:]

    flagged_categories = []
    for e in to_draft:
        message = draft_message(
            category=e["category"],
            previous_revenue=e["previous_revenue"],
            current_revenue=e["current_revenue"],
            mom_pct=e["mom_pct"],
            month=month,
            prev_month=prev_month_label,
        )
        flagged_categories.append({
            "category": e["category"],
            "mom_pct": e["mom_pct"],
            "previous_revenue": e["previous_revenue"],
            "current_revenue": e["current_revenue"],
            "drafted": True,
            "message": message,
        })

    # Subtask 7: the rest are suppressed (no message drafted)
    suppressed_categories = [e["category"] for e in to_suppress]

    # Subtask 8: structured output
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":
    FIXTURES = os.path.join(BASE, "fixtures")
    P2_FIXTURES = os.path.join(BASE, "..", "part2_engine", "fixtures")

    print("=== Scenario 1: April -> May ===")
    print(json.dumps(run("May",
                         os.path.join(FIXTURES, "april.csv"),
                         os.path.join(FIXTURES, "may.csv")), indent=2))

    print("\n=== Scenario 2: May -> June ===")
    print(json.dumps(run("June",
                         os.path.join(FIXTURES, "may.csv"),
                         os.path.join(FIXTURES, "june.csv")), indent=2))

    print("\n=== Scenario 3: Corrupted feed as current month ===")
    print(json.dumps(run("July",
                         os.path.join(FIXTURES, "may.csv"),
                         os.path.join(P2_FIXTURES, "corrupted_feed.csv")), indent=2))