# Agent Specification — Meesho Reseller Growth Monitoring Agent

## 4.1 — Core components

### Goal
Keep Meesho category managers informed of any category whose
month-on-month revenue moves beyond the 8% threshold, with a human
approving every message before it goes out.

### Tools
The agent calls these concrete functions, reused unmodified from earlier
Parts:

| Tool | Source | Purpose |
|---|---|---|
| `validate_feed(csv_path)` | Part 2 | Input guardrail over the current month's feed |
| `mom_growth(previous, current)` | Part 2 | Month-on-Month growth calculation |
| `is_flagged(mom_pct, threshold=8.0)` | Part 2 | Three-way classification of a growth percentage |
| `draft_message(...)` | Part 3 | Offline template-fill function that drafts the stakeholder update |

### Memory / State
Between monthly runs, the agent must persist **the previous month's
revenue per category**, so the next run's `mom_growth` call has something
to compare the new month against. In this mock runner that state is
passed in explicitly as `previous_month_csv`; in a production version it
would be the last run's `current_month_csv` (or a small key-value store
of `{category: revenue}`), refreshed after every successful run.

### Feedback Loop
Every drafted message is held, never auto-sent. This is simulated by the
`drafted: true` flag and `action_taken: "drafted_and_held_for_approval"`
in the JSON output — a human (the category manager or a reviewer) must
read and approve each draft before it is considered "sent." No actual
email/SMTP/Gmail integration exists or is in scope; approval is a manual
step downstream of this JSON output.

## 4.2 — Planner (ordered subtasks)

1. Load the current month's revenue feed and run `validate_feed` on it.
2. If invalid, **Hard Stop** and report the validation errors — do not
   proceed to any later step.
3. If valid, compute `mom_growth` for every category against the previous
   month's revenue for that category.
4. Run `is_flagged` on every category's MoM percentage.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a message (via Part 3's template) for **at most the top 3**
   flagged categories by magnitude — this cap exists specifically to
   prevent the notification-flooding failure mode of drafting (and
   eventually sending) one message per flagged item with no limit.
7. Log any remaining flagged categories beyond the cap as
   `"suppressed, review manually"` — no message is drafted for them.
8. Separately, log any category whose `is_flagged` result is
   `"escalate_exact_boundary"` into `escalated_categories`, without
   drafting a message for it. An exact-boundary category is neither
   flagged nor not_flagged, so it must never be silently dropped from
   both lists or mistaken for either one.
9. Emit one structured JSON object summarizing the run.

## 4.3 — Structured JSON Output Schema

Every run of the mock agent runner — whether it succeeds or Hard Stops —
emits one JSON object with exactly these top-level keys:

| Key | Meaning |
|---|---|
| `run_month` | The month being processed (e.g. `"May"`) |
| `validation_status` | `"valid"` or `"invalid"` |
| `validation_errors` | List of error strings; empty on success |
| `flagged_categories` | List of objects: `category`, `mom_pct`, `previous_revenue`, `current_revenue`, `drafted` (boolean), and `message` if drafted |
| `suppressed_categories` | List of category names beyond the top-3 cap; empty if nothing was suppressed |
| `escalated_categories` | List of category names whose result was `"escalate_exact_boundary"`; empty unless a real transition happens to land exactly on the threshold |
| `action_taken` | `"drafted_and_held_for_approval"` or `"hard_stop"` |

Keeping this exact same shape on every run — success or failure — is what
makes the output reliably usable by whatever consumes it next (a
dashboard, a log, a human reviewer): they always know which fields to
look for, without needing separate handling for the success case versus
the failure case.

## 4.4 — Guardrails

**Input guardrail:** `validate_feed` must pass (return `(True, [])`) on
the current month's feed before any MoM computation, drafting, or logging
happens. An invalid feed halts the entire run.

**Action guardrail:** no message is ever auto-sent. Every drafted message
is only ever drafted and held for human approval — there is no code path
in this agent that sends anything.

**Output guardrail:** every number that appears in a drafted message must
trace back to a Part 1/Part 2 value (`category`, `mom_pct`,
`previous_revenue`, `current_revenue`). No invented figures, no numbers
pulled from anywhere else.

## 4.5 — Success and error stopping conditions

- **Success:** drafts are produced (or correctly zero drafts, if nothing
  crossed the threshold), with every number in every draft traceable to
  Part 1/Part 2 data. `action_taken = "drafted_and_held_for_approval"`.
- **Error:** `validate_feed` returns `False` for the current month's feed.
  This is a **Hard Stop** — the run reports the validation errors and
  takes no further action (`action_taken = "hard_stop"`). It is never
  treated as a silent skip; the errors must be surfaced.

## 4.6 — Given-When-Then specs (agent-level, reused from Part 2)

1. **GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to
   185107.61, **WHEN** the agent computes MoM growth and classifies it,
   **THEN** the agent records `mom_pct = 77.1` and classification
   `"flagged"`, and — since it is within the top 3 by magnitude — drafts a
   message for it.
2. **GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11
   to 37559.07, **WHEN** the agent computes MoM growth and classifies it,
   **THEN** the agent records `mom_pct = 5.67` and classification
   `"not_flagged"`, and takes no drafting or suppression action for it —
   it appears in neither `flagged_categories` nor
   `suppressed_categories`.
3. **GIVEN** a synthetic category pair `previous=100000, current=108000`,
   **WHEN** the agent computes MoM growth and classifies it, **THEN** the
   agent records `mom_pct = 8.0`, classification
   `"escalate_exact_boundary"`, and logs the category into
   `escalated_categories` without drafting a message and without placing
   it in `flagged_categories` or `suppressed_categories`.
4. **GIVEN** the corrupted feed fixture (containing a negative-revenue
   row, a missing-category row, and a missing-revenue row) as the current
   month's feed, **WHEN** the agent runs `validate_feed` on it as step 1,
   **THEN** the agent Hard Stops with `validation_status = "invalid"`,
   the 3 expected error strings in `validation_errors`, empty
   `flagged_categories` and `suppressed_categories`, and
   `action_taken = "hard_stop"` — no MoM computation is attempted on
   invalid data.

These four specs are implemented as executable assertions in
`test_scenarios.py`, alongside the two real monthly scenarios
(April→May, May→June).