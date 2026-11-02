from datetime import date


def assess_observations(observations: list[dict]) -> dict[str, object]:
    dates = [item["observed_on"] for item in observations]
    unique_dates = len(set(dates)) == len(dates)
    ordered = dates == sorted(dates)
    complete = all(
        item.get("steps") is not None and item.get("sleep_hours") is not None
        for item in observations
    )
    return {
        "agent": "data_quality",
        "valid": unique_dates and complete and len(observations) >= 14,
        "observations": len(observations),
        "unique_dates": unique_dates,
        "chronological": ordered,
        "complete": complete,
        "as_of": max(dates) if dates else date.today(),
    }
