"""
Deterministic, fully offline template-fill function implementing the prompt
in prompt_pack.md. No network call, no API key. Part 4 imports this for
drafting messages.
"""


def draft_message(category: str, previous_revenue: float, current_revenue: float,
                  mom_pct: float, month: str, prev_month: str) -> str:
    direction = "grew" if mom_pct > 0 else "declined"

    context = (
        f"Context: This update covers {category} revenue for {month}, "
        f"compared against {prev_month}."
    )
    insight = (
        f"Insight (Fact): {category} revenue {direction} by {mom_pct}% "
        f"month-on-month, moving from INR {previous_revenue:,.2f} in "
        f"{prev_month} to INR {current_revenue:,.2f} in {month}."
    )
    if mom_pct > 0:
        implication = (
            f"Implication (Hypothesis): the {mom_pct}% jump may reflect "
            f"seasonal demand or a listing/pricing change in {category}; "
            f"recommend the regional manager check current stock coverage "
            f"and reorder lead times for {category} before {month} closes, "
            f"so the gain isn't lost to stockouts."
        )
    else:
        implication = (
            f"Implication (Hypothesis): the {mom_pct}% decline may reflect "
            f"reduced listing visibility, price competitiveness, or reseller "
            f"activity in {category}; recommend the regional manager audit "
            f"active {category} listings and top reseller activity for "
            f"{month} within the next reporting cycle."
        )

    return f"[ALERT] {category} | {month} vs {prev_month} | MoM: {mom_pct}%\n{context} {insight} {implication}"