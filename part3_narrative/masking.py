"""
Part 3.4 -- Masking policy.
"""


def alias_for(reseller_id: str) -> str:
    """RS019 -> ALIAS-19, RS006 -> ALIAS-06."""
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """Returns False if any raw reseller_name appears verbatim inside text."""
    for name in reseller_names:
        if name in text:
            return False
    return True


if __name__ == "__main__":
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"

    top_resellers = [
        ("RS019", "West", 75295.09),
        ("RS022", "West", 73882.33),
        ("RS012", "South", 69936.46),
        ("RS006", "North", 64238.97),
        ("RS005", "North", 61825.02),
    ]
    raw_names = [
        "Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6",
        "Lucknow Reseller 6", "Jaipur Reseller 5",
    ]

    lines = ["Top resellers by total spend this quarter:"]
    for reseller_id, region, spend in top_resellers:
        lines.append(f"  {alias_for(reseller_id)} ({region} region): INR {spend:,.2f}")
    final_narrative = "\n".join(lines)
    print(final_narrative)

    # Positive case
    assert assert_no_raw_names_leak(final_narrative, raw_names) is True
    print("\nassert_no_raw_names_leak(final_narrative, raw_names) == True  [PASS]")

    # Negative case
    leaking_narrative = final_narrative + "\nTop performer: Mumbai Reseller 1"
    assert assert_no_raw_names_leak(leaking_narrative, raw_names) is False
    print("assert_no_raw_names_leak(leaking_narrative, raw_names) == False [PASS]")