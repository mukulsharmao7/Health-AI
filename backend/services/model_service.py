from pathlib import Path
import joblib
import pandas as pd

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Saved model location
MODEL_PATH = BASE_DIR / "models" / "isolation_forest.joblib"

# Load model artifact
artifact = joblib.load(MODEL_PATH)

model = artifact["model"]
FEATURES = artifact["features"]


def predict_anomaly(steps_deviation_7d_pct: float,
                    sleep_deviation_7d_pct: float) -> dict:
    """
    Predict whether a wearable activity-sleep pattern
    is unusual relative to the model's learned patterns.
    """

    input_data = pd.DataFrame(
        [[steps_deviation_7d_pct, sleep_deviation_7d_pct]],
        columns=FEATURES
    )

    prediction = int(model.predict(input_data)[0])
    anomaly_score = float(model.decision_function(input_data)[0])

    return {
        "anomaly_label": prediction,
        "anomaly_score": anomaly_score,
        "interpretation": (
            "unusual pattern flagged"
            if prediction == -1
            else "no unusual pattern flagged"
        )
    }