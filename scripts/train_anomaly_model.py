"""Train the deployable Isolation Forest from the processed research dataset."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "daily_features.csv"
MODEL_PATH = ROOT / "models" / "isolation_forest.joblib"
FEATURES = ["steps_deviation_7d_pct", "sleep_deviation_7d_pct"]


def train() -> dict[str, object]:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Processed dataset not found at {DATA_PATH}. Complete notebooks 01–07 first."
        )

    data = pd.read_csv(DATA_PATH)
    required = {"Id", *FEATURES}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Processed dataset is missing required columns: {sorted(missing)}")

    participant_ids = sorted(data["Id"].dropna().unique())
    if len(participant_ids) <= 3:
        raise ValueError("At least four participants are required for the established holdout.")
    holdout_ids = set(participant_ids[-3:])
    train_data = data.loc[~data["Id"].isin(holdout_ids), FEATURES].dropna()
    if len(train_data) < 10:
        raise ValueError("At least ten valid training observations are required.")

    model = IsolationForest(n_estimators=100, contamination="auto", random_state=42)
    model.fit(train_data)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH, compress=3)
    return {"model_path": str(MODEL_PATH), "training_rows": len(train_data)}


if __name__ == "__main__":
    result = train()
    print(f"Model saved to {result['model_path']}")
    print(f"Training rows: {result['training_rows']}")
