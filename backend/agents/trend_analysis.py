from statistics import mean


def compare_windows(observations: list[dict], metric: str, agent_name: str) -> dict[str, object]:
    ordered = sorted(observations, key=lambda item: item["observed_on"])
    baseline = mean(float(item[metric]) for item in ordered[-14:-7])
    recent = mean(float(item[metric]) for item in ordered[-7:])
    change_pct = ((recent - baseline) / baseline * 100) if baseline else None
    return {
        "agent": agent_name,
        "baseline_7d_average": round(baseline, 2),
        "recent_7d_average": round(recent, 2),
        "change_pct": round(change_pct, 2) if change_pct is not None else None,
        "interpretation": (
            "percentage change unavailable because the earlier average is zero"
            if change_pct is None
            else "recent average compared with the preceding 7 observations"
        ),
    }
