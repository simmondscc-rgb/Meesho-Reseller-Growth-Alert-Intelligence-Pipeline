import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from growth_engine import mom_growth, is_flagged, validate_feed

FIXTURES = os.path.join(BASE, "fixtures")

print(mom_growth(104520.77, 185107.61), is_flagged(mom_growth(104520.77, 185107.61)))
print(mom_growth(35542.11, 37559.07), is_flagged(mom_growth(35542.11, 37559.07)))
print(mom_growth(100000, 108000), is_flagged(mom_growth(100000, 108000)))
print(validate_feed(os.path.join(FIXTURES, "corrupted_feed.csv")))
print(validate_feed(os.path.join(FIXTURES, "monthly_category_revenue.csv")))