from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.model_service import predict_anomaly



router = APIRouter()


class PredictionRequest(BaseModel):
    steps_deviation_7d_pct: float = Field(
        description="Percentage deviation in steps from personal baseline"
    )
    sleep_deviation_7d_pct: float = Field(
        description="Percentage deviation in recorded sleep from personal baseline"
    )


@router.post("/predict")
def predict_health_pattern(request: PredictionRequest):
    result = predict_anomaly(
        steps_deviation_7d_pct=request.steps_deviation_7d_pct,
        sleep_deviation_7d_pct=request.sleep_deviation_7d_pct
    )

    return result