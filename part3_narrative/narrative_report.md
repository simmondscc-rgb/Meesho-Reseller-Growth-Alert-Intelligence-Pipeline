# Narrative Report

Two worked examples of `prompt_pack.md`'s template applied to real,
verified numbers from Part 1/Part 2 — one flagged in the positive
direction, one in the negative — each self-scored against the 4-criterion
checklist, followed by the chart-choice justification for three business
questions.

## 3.2 Worked narratives

### Narrative 1 — May Ethnic Wear (+77.1% MoM, flagged)

**Context:** This update covers Ethnic Wear revenue for May, compared
against April.

**Insight (Fact):** Ethnic Wear revenue grew by **77.1%** month-on-month,
moving from INR 104,520.77 in April to INR 185,107.61 in May.

**Implication (Hypothesis):** the 77.1% jump may reflect seasonal demand or
a listing/pricing change in Ethnic Wear — the data does not tell us the
cause. Recommend the regional manager check current stock coverage and
reorder lead times for Ethnic Wear before May closes, so the gain is not
lost to stockouts in June.

**Self-score against the 4-criterion checklist:**
- *Specificity* — Passes: names the exact category (Ethnic Wear), the exact
  percentage (77.1%), and both months (April, May) rather than speaking in
  generalities.
- *Audience fit* — Passes: written in plain business language ("stock
  coverage", "reorder lead times") a regional manager acts on daily, with
  no SQL/statistics jargon.
- *Completeness* — Passes: all three sections (Context, Insight,
  Implication) are present and each is non-empty.
- *Actionability* — Passes: the recommendation names a concrete action
  (check stock coverage and reorder lead times) with a deadline (before May
  closes), not a vague "look into ethnic wear."

### Narrative 2 — June Ethnic Wear (-58.74% MoM, flagged)

**Context:** This update covers Ethnic Wear revenue for June, compared
against May.

**Insight (Fact):** Ethnic Wear revenue declined by **-58.74%**
month-on-month, moving from INR 185,107.61 in May to INR 76,371.53 in
June.

**Implication (Hypothesis):** the -58.74% decline may reflect reduced
listing visibility, weaker price competitiveness, or lower reseller
activity in Ethnic Wear — again, this is a hypothesis, not a proven cause.
Recommend the regional manager audit active Ethnic Wear listings and
top-reseller activity for June within the next reporting cycle, to
distinguish a demand problem from a supply/listing problem.

**Self-score against the 4-criterion checklist:**
- *Specificity* — Passes: names the exact category, the exact percentage
  (-58.74%), and both months (May, June).
- *Audience fit* — Passes: framed as an operational question ("audit active
  listings and top-reseller activity") rather than a statistical one.
- *Completeness* — Passes: Context, Insight, and Implication are all
  present.
- *Actionability* — Passes: the recommendation specifies exactly what to
  check (active listings, top-reseller activity) and by when (next
  reporting cycle).

## 3.3 Chart-choice justification

**1. "Which month had the highest total revenue?"**
(April = INR 419,417.43, May = INR 444,594.25, June = INR 398,055.24)

Use a **vertical bar chart** with one bar per month. This is a **univariate**
comparison — a single numeric variable (total revenue) across three
categorical buckets (month) — and a bar chart lets a reader identify the
tallest bar, and therefore the answer, in well under 10 seconds. The y-axis
must start at zero so bar heights are visually proportional to their real
values (starting above zero would exaggerate the difference between May and
June). No legend is needed since there is only one series (revenue), and a
flat 2D bar avoids the distorted comparisons a 3D bar chart would introduce.

**2. "What percentage share does Ethnic Wear represent of April's total
revenue?"** (INR 104,520.77 of INR 419,417.43 = 24.92%)

Use a **single annotated horizontal bar (part-to-whole bar)** showing Ethnic
Wear's share against the remaining 75.08%, with the 24.92% figure labeled
directly on the bar — not a pie/donut chart. This is a **bivariate**,
part-to-whole question (one category's revenue vs. the total), and while
part-to-whole is the classic "reach for a pie chart" instinct, a labeled bar
is easier to read precisely within 10 seconds than judging a pie slice's
angle, and it still starts from a zero-based, linear scale. A legend is
unnecessary since the bar's own label carries the answer.

**3. "How do the four regions compare on total revenue?"**
(North = INR 337,125.46, West = INR 333,106.33, South = INR 316,736.68,
East = INR 275,098.45)

Use a **vertical bar chart**, one bar per region, sorted descending by
revenue. This is a **bivariate** comparison (region, a categorical
variable, against total revenue, a numeric variable) with four
roughly-similar values, so a sorted bar chart makes the ranking obvious at
a glance — the message ("North leads, East trails") is clear well within
10 seconds. The y-axis starts at zero (the four values are close together,
so a non-zero baseline would visually overstate the differences between
regions), it is rendered in flat 2D, and no legend is required since all
four bars represent the same single metric (revenue).