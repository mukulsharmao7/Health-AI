from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "isolation_forest.joblib"
FEATURES = ("steps_deviation_7d_pct", "sleep_deviation_7d_pct")


class ModelUnavailableError(RuntimeError):
    """Raised when the deployable model artifact is absent or invalid."""


@lru_cache(maxsize=1)
def _load_model():
    if not MODEL_PATH.is_file():
        raise ModelUnavailableError("The anomaly model artifact is not installed.")
    try:
        artifact = joblib.load(MODEL_PATH)
        model = artifact["model"]
        features = tuple(artifact["features"])
    except Exception as exc:
        raise ModelUnavailableError("The anomaly model artifact could not be loaded.") from exc
    if features != FEATURES or not hasattr(model, "predict"):
        raise ModelUnavailableError("The anomaly model artifact has an incompatible schema.")
    return model


def model_is_available() -> bool:
    try:
        _load_model()
    except ModelUnavailableError:
        return False
    return True


def predict_anomaly(steps_deviation_7d_pct: float, sleep_deviation_7d_pct: float) -> dict:
    """Flag unusual wearable patterns relative to the trained research model."""
    model = _load_model()
    input_data = pd.DataFrame(
        [[steps_deviation_7d_pct, sleep_deviation_7d_pct]], columns=FEATURES
    )
    prediction = int(model.predict(input_data)[0])
    anomaly_score = float(model.decision_function(input_data)[0])
    return {
        "anomaly_label": prediction,
        "anomaly_score": anomaly_score,
        "interpretation": (
            "unusual pattern flagged" if prediction == -1 else "no unusual pattern flagged"
        ),
        "notice": "Research prototype output; not a diagnosis or medical advice.",
    }
