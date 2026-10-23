# 🏥 Health-AI

Health-AI is an AI-powered personalized health platform that analyzes longitudinal wearable data to detect meaningful changes from an individual's personal health baseline and provide evidence-grounded health insights using Machine Learning, Deep Learning, RAG, and Agentic AI.

## 📅 Development Log

| Day | Date | Work Done |
|---|---|---|
| Day 1 | 24 Sep 2026 | Project initialization, virtual environment setup, dependencies configuration, environment setup, Git repository initialization and initial commit |
| Day 2 | 26 Sep 2026 | FastAPI backend foundation, API routing, health-check endpoint, CORS configuration, API versioning and backend structure |
| Day 3 | 27 Sep 2026 | Wearable health dataset selection, dataset analysis, raw data organization, longitudinal health research problem definition |
| Day 4 | 28 Sep 2026 | Exploratory data analysis, participant coverage analysis, activity trend visualization, daily step distribution, steps-calories relationship and correlation analysis |
| Day 5 | 1 Oct 2026 | Data quality auditing, missing-value analysis, duplicate detection and removal, datetime standardization, chronological sorting and processed dataset generation |
| Day 6 | 2 Oct 2026 | Feature engineering, personalized 7-observation baselines, activity and sleep deviation features, rolling trends, health ratios and ML-ready feature dataset generation |
| Day 7 | 12 Oct 2026 | Personal-baseline deviation analysis, sustained activity and sleep deviation rules, preliminary alert flags and ML problem formulation |
| Day 8 | 13 Oct 2026 | ML input preparation, Isolation Forest anomaly detection, anomaly inspection and comparison with rule-based personalized deviation alerts |
| Day 9 | 14 Oct 2026 | Anomaly visualization, scatter-plot interpretation, anomaly-score ranking and inspection of unusual personalized activity-sleep patterns |
| Day 10 | 14 Oct 2026 | Extreme anomaly inspection, low recorded-sleep quality flags, data-quality overlap analysis and participant-level evaluation planning |
| Day 11 | 15 Oct 2026 | Participant-level holdout evaluation, train-only Isolation Forest fitting, unseen-participant anomaly scoring and exploratory comparison with rule-based deviation alerts |
| Day 12 | 16 Oct 2026 | Previous-observation rolling features, missing-history analysis and expanded Isolation Forest feature experiment |
| Day 13 | 17 Oct 2026 | Participant-level holdout comparison of basic and expanded Isolation Forest feature sets, common-test-set analysis and anomaly agreement assessment |
| Day 14 | 17 Oct 2026 | Saved Isolation Forest model, reusable prediction service, FastAPI prediction endpoint and successful Swagger API test |
| Day 15 | 18 Oct 2026 | Prediction input validation, numeric boundary checks, API exception handling, server-side error logging and regression testing |
| Day 16 | 19 Oct 2026 | Time-series sequence generation, participant-level data splitting, PyTorch neural network training and comparison against a mean-prediction baseline |
| Day 17 | 23 Oct 2026 | StandardScaler-based feature scaling, training-only scaler fitting, participant-level split verification, scaled PyTorch model training and mean-baseline evaluation |