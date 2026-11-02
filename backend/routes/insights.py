from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from backend.services.insight_workflow import analyze_observations

router = APIRouter()


class DailyObservation(BaseModel):
    observed_on: date
    steps: int = Field(ge=0, le=200_000)
    sleep_hours: float = Field(ge=0, le=24, allow_inf_nan=False)


class InsightRequest(BaseModel):
    observations: list[DailyObservation] = Field(min_length=14, max_length=60)

    @field_validator("observations")
    @classmethod
    def require_unique_dates(cls, observations):
        dates = [item.observed_on for item in observations]
        if len(dates) != len(set(dates)):
            raise ValueError("Each observation must use a unique date.")
        return observations


@router.post("/insights/analyze")
def analyze_health_patterns(request: InsightRequest):
    observations = [item.model_dump() for item in request.observations]
    return analyze_observations(observations)
