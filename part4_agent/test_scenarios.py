"""
Given-When-Then assertions for mock_agent_runner.run(), reusing the same
four specs documented in agent_spec.md section 4.4 and growth_engine's
test suite -- phrased here as agent-level checks on the full JSON output,
not just the underlying growth_engine functions.

Run with: python test_scenarios.py   (from inside part4_agent/)
"""

import csv
import os
import shutil
import tempfile

from mock_agent_runner import run

BASE = os.path.dirname(os.path.abspath(__file__))
P2_FIXTURES = os.path.join(BASE, "..", "part2_engine", "fixtures")


def test_april_to_may_drafts_top_3_in_order():
    # GIVEN the April -> May revenue feeds
    # WHEN the agent runs for May
    result = run(
        month="May",
        previous_month_csv=os.path.join(BASE, "april_revenue.csv"),
        current_month_csv=os.path.join(BASE, "may_revenue.csv"),
    )
    # THEN validation passes, exactly 3 drafted categories in this order,
    # and exactly 2 suppressed
    assert result["validation_status"] == "valid"
    drafted_names = [c["category"] for c in result["flagged_categories"]]
    assert drafted_names == ["Ethnic Wear", "Western Wear", "Kids Wear"], drafted_names
    assert all(c["drafted"] is True for c in result["flagged_categories"])
    assert set(result["suppressed_categories"]) == {"Beauty & Personal Care", "Home & Kitchen"}
    assert result["escalated_categories"] == []
    assert result["action_taken"] == "drafted_and_held_for_approval"


def test_may_to_june_drafts_top_3_in_order():
    # GIVEN the May -> June revenue feeds
    # WHEN the agent runs for June
    result = run(
        month="June",
        previous_month_csv=os.path.join(BASE, "may_revenue.csv"),
        current_month_csv=os.path.join(BASE, "june_revenue.csv"),
    )
    # THEN exactly 3 drafted in this order, 1 suppressed, Beauty in neither
    drafted_names = [c["category"] for c in result["flagged_categories"]]
    assert drafted_names == ["Ethnic Wear", "Home & Kitchen", "Kids Wear"], drafted_names
    assert result["suppressed_categories"] == ["Western Wear"]
    all_mentioned = drafted_names + result["suppressed_categories"]
    assert "Beauty & Personal Care" not in all_mentioned
    assert result["escalated_categories"] == []


def test_corrupted_feed_hard_stops():
    # GIVEN the corrupted feed fixture as the current month's feed
    # WHEN the agent runs
    result = run(
        month="July",
        previous_month_csv=os.path.join(BASE, "may_revenue.csv"),
        current_month_csv=os.path.join(P2_FIXTURES, "corrupted_feed.csv"),
    )
    # THEN it Hard Stops with exactly the 3 expected errors and empty lists
    assert result["validation_status"] == "invalid"
    assert result["action_taken"] == "hard_stop"
    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]
    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []


def test_exact_boundary_is_escalated_not_flagged_or_suppressed():
    # GIVEN a synthetic category pair at exactly the 8.0% boundary
    tmpdir = tempfile.mkdtemp()
    try:
        prev_path = os.path.join(tmpdir, "prev.csv")
        curr_path = os.path.join(tmpdir, "curr.csv")
        with open(prev_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["month", "category", "revenue", "n_orders"])
            w.writerow(["Test", "Boundary Cat", 100000, 10])
        with open(curr_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["month", "category", "revenue", "n_orders"])
            w.writerow(["Test2", "Boundary Cat", 108000, 10])

        # WHEN the agent runs
        result = run(month="Test2", previous_month_csv=prev_path, current_month_csv=curr_path)

        # THEN it lands only in escalated_categories -- never flagged, never suppressed
        assert result["escalated_categories"] == ["Boundary Cat"]
        assert result["flagged_categories"] == []
        assert result["suppressed_categories"] == []
    finally:
        shutil.rmtree(tmpdir)


if __name__ == "__main__":
    tests = [
        test_april_to_may_drafts_top_3_in_order,
        test_may_to_june_drafts_top_3_in_order,
        test_corrupted_feed_hard_stops,
        test_exact_boundary_is_escalated_not_flagged_or_suppressed,
    ]
    for t in tests:
        t()
        print(f"PASSED: {t.__name__}")
    print("\nAll scenario tests passed.")
