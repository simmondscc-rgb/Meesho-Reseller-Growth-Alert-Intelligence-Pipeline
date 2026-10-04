"""
Given-When-Then tests for growth_engine.py
Run with: python3 test_growth_engine.py   (from inside part2_engine/)
     or:  pytest part2_engine/test_growth_engine.py
"""

import os
from growth_engine import mom_growth, is_flagged, validate_feed

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def test_case_1_april_to_may_ethnic_wear_flagged():
    # GIVEN April->May Ethnic Wear revenue moves from 104520.77 to 185107.61
    previous, current = 104520.77, 185107.61
    # WHEN mom_growth then is_flagged run on it
    growth = mom_growth(previous, current)
    flag = is_flagged(growth)
    # THEN mom_growth returns 77.1 and is_flagged returns "flagged"
    assert growth == 77.1, f"expected 77.1, got {growth}"
    assert flag == "flagged", f"expected 'flagged', got {flag}"


def test_case_2_may_to_june_beauty_not_flagged():
    # GIVEN May->June Beauty & Personal Care revenue moves from 35542.11 to 37559.07
    previous, current = 35542.11, 37559.07
    # WHEN evaluated
    growth = mom_growth(previous, current)
    flag = is_flagged(growth)
    # THEN mom_growth returns 5.67 and is_flagged returns "not_flagged"
    assert growth == 5.67, f"expected 5.67, got {growth}"
    assert flag == "not_flagged", f"expected 'not_flagged', got {flag}"


def test_case_3_exact_boundary_escalates():
    # GIVEN a synthetic pair previous=100000, current=108000
    previous, current = 100000, 108000
    # WHEN evaluated
    growth = mom_growth(previous, current)
    flag = is_flagged(growth)
    # THEN mom_growth returns exactly 8.0 and is_flagged returns "escalate_exact_boundary"
    assert growth == 8.0, f"expected 8.0, got {growth}"
    assert flag == "escalate_exact_boundary", f"expected 'escalate_exact_boundary', got {flag}"
    assert flag != "flagged"
    assert flag != "not_flagged"


def test_case_4_corrupted_feed_validation():
    # GIVEN the corrupted feed fixture
    path = os.path.join(FIXTURES, "corrupted_feed.csv")
    # WHEN validate_feed runs on it
    ok, errors = validate_feed(path)
    # THEN it returns (False, errors) with exactly 3 entries in this order
    assert ok is False
    assert len(errors) == 3, f"expected 3 errors, got {len(errors)}: {errors}"
    assert errors[0] == "line 3: negative revenue (-4200.0) for category=Western Wear"
    assert errors[1] == "line 4: missing category (month=July)"
    assert errors[2] == "line 6: missing revenue (category=Home & Kitchen)"


def test_clean_feed_passes_validation():
    # GIVEN Part 1's validated monthly_category_revenue.csv
    path = os.path.join(FIXTURES, "monthly_category_revenue.csv")
    # WHEN validate_feed runs on it
    ok, errors = validate_feed(path)
    # THEN there should be zero errors
    assert ok is True
    assert errors == []


if __name__ == "__main__":
    tests = [
        test_case_1_april_to_may_ethnic_wear_flagged,
        test_case_2_may_to_june_beauty_not_flagged,
        test_case_3_exact_boundary_escalates,
        test_case_4_corrupted_feed_validation,
        test_clean_feed_passes_validation,
    ]
    for t in tests:
        t()
        print(f"PASSED: {t.__name__}")
    print("\nAll tests passed.")