from datetime import date, timedelta

from backend.services.insight_workflow import analyze_observations


def observations(step_values=None):
    start = date(2026, 10, 20)
    steps = step_values or [5000] * 7 + [6500] * 7
    return [
        {"observed_on": start + timedelta(days=index), "steps": steps[index], "sleep_hours": 7.0}
        for index in range(14)
    ]


def test_coordinator_runs_quality_activity_sleep_and_model_agents():
    result = analyze_observations(observations())
    assert result["status"] == "complete"
    assert result["quality"]["agent"] == "data_quality"
    assert result["activity"]["agent"] == "activity_trend"
    assert result["sleep"]["agent"] == "sleep_trend"
    assert result["pattern_model"]["anomaly_label"] in (-1, 1)


def test_coordinator_flags_duplicate_date_as_invalid():
    items = observations()
    items[0]["observed_on"] = items[1]["observed_on"]
    result = analyze_observations(items)
    assert result["status"] == "insufficient_or_invalid_data"
    assert result["quality"]["unique_dates"] is False
