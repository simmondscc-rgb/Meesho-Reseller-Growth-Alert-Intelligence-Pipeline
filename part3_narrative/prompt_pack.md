# Reusable Prompt Pack: Flagged-Category Stakeholder Update

## Trigger
A category's `is_flagged()` result (from Part 2's `growth_engine`) is exactly
`"flagged"` for the current reporting month. (Categories returning
`"not_flagged"` or `"escalate_exact_boundary"` do not trigger this prompt —
the latter is routed to human review instead, per the agent spec in Part 4.)

## Input list
Every placeholder the prompt needs, all of which must trace back to a Part
1/Part 2 value — nothing else is permitted to appear in the output:

- `{category}` — the category name, e.g. "Ethnic Wear"
- `{month}` — the current reporting month, e.g. "May"
- `{prev_month}` — the prior month being compared against, e.g. "April"
  (needed so the narrative can say "May vs. April" explicitly)
- `{previous_revenue}` — revenue for `{prev_month}` (from Part 1's
  `monthly_category_revenue.csv`)
- `{current_revenue}` — revenue for `{month}` (same source)
- `{mom_pct}` — the signed Month-on-Month growth percentage from
  `mom_growth()` (Part 2)

## Prompt
```
You are drafting a short stakeholder update for a regional category manager
at Meesho. Use ONLY the values supplied below. Do not state any number that
is not one of these six placeholders. Do not invent a cause, a competitor
action, a marketing event, or any other fact not given here.

Category: {category}
Comparison: {month} vs. {prev_month}
Previous revenue ({prev_month}): INR {previous_revenue}
Current revenue ({month}): INR {current_revenue}
Month-on-Month change: {mom_pct}%

Write the update in exactly three labeled parts:
1. Context — one sentence stating what is being measured and over what
   period, using {category}, {month}, and {prev_month}.
2. Insight — one sentence stating the {mom_pct}% change as a FACT (label it
   "Fact:"), citing {previous_revenue} and {current_revenue}.
3. Implication — one or two sentences giving a specific, actionable next
   step for the regional manager (e.g. "review [X]", "check [Y] before
   [deadline]"). If the recommendation implies a cause the data alone does
   not prove, label that sentence "Hypothesis:" explicitly.

Do not reference any reseller by raw name — if a reseller must be mentioned,
use alias_for(reseller_id) (Part 3.4) instead.
```

## Checklist
Run all of the following against the drafted output before it is used or
sent to anyone:

1. **Number-fidelity check** — every numeric figure in the draft matches one
   of the six supplied placeholder values exactly (no rounding drift, no
   invented figures).
2. **Fact/hypothesis labeling check** — every claim in the draft is
   explicitly labeled either "Fact:" (only for values taken directly from
   the placeholders) or "Hypothesis:" (for any inferred cause).
3. **Actionability check** — the Implication section names a specific,
   concrete action (a thing to check, review, or do, with an object and,
   where relevant, a timeframe) rather than a vague statement like "look
   into this."
4. **Masking check** — `assert_no_raw_names_leak()` (Part 3.4) returns
   `True` on the draft; no raw `reseller_name` string appears verbatim.
5. **Structure check** — the draft contains all three labeled sections
   (Context, Insight, Implication) in order, and none is empty.
