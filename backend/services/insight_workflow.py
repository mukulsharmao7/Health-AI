from backend.agents.data_quality import assess_observations
from backend.agents.trend_analysis import compare_windows
from backend.services.model_service import predict_anomaly

NOTICE = "Research prototype only; these observations do not diagnose or rule out illness."


def analyze_observations(observations: list[dict]) -> dict[str, object]:
    quality = assess_observations(observations)
    if not quality["valid"]:
        return {"status": "insufficient_or_invalid_data", "quality": quality, "notice": NOTICE}

    ordered = sorted(observations, key=lambda item: item["observed_on"])
    activity = compare_windows(ordered, "steps", "activity_trend")
    sleep = compare_windows(ordered, "sleep_hours", "sleep_trend")
    anomaly = None
    if activity["change_pct"] is not None and sleep["change_pct"] is not None:
        anomaly = predict_anomaly(
            steps_deviation_7d_pct=activity["change_pct"],
            sleep_deviation_7d_pct=sleep["change_pct"],
        )
    return {
        "status": "complete",
        "workflow": "deterministic_multi_agent_v1",
        "quality": quality,
        "activity": activity,
        "sleep": sleep,
        "pattern_model": anomaly,
        "notice": NOTICE,
    }
