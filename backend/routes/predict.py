from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.model_service import predict_anomaly



router = APIRouter()


from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    steps_deviation_7d_pct: float = Field(
        ge=-100,
        le=500,
        description="Percentage deviation in steps from personal baseline"
    )

    sleep_deviation_7d_pct: float = Field(
        ge=-100,
        le=500,
        description="Percentage deviation in recorded sleep from personal baseline"
    )
    
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


@router.post("/predict")
def predict_health_pattern(request: PredictionRequest):
    try:
        return predict_anomaly(
            steps_deviation_7d_pct=request.steps_deviation_7d_pct,
            sleep_deviation_7d_pct=request.sleep_deviation_7d_pct
        )
    except Exception:
        logger.exception("Health pattern prediction failed")
        raise HTTPException(
            status_code=500,
            detail="Prediction could not be completed. Please try again."
        )