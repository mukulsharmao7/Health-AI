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
| Day 18 | 30 Oct 2026 | Prediction-versus-actual visualization, absolute error analysis, participant-wise model evaluation and ML observability fundamentals |
| Day 19 | 1 Nov 2026 | Independent target-scaling experiment, participant-level sequence splitting, input and target standardization, PyTorch training, inverse transformation and baseline comparison |
| Day 20 | 1 Nov 2026 | Dataset integrity diagnostics, participant eligibility analysis, personal-baseline validation, temporal consistency checks and ML foundation review |
| Day 21 | 2 Nov 2026 | PostgreSQL 18.6 database created, environment-based SQLAlchemy configuration and verified connection on port 5433; `.env` remains ignored by Git |
| Day 22 | 2 Nov 2026 | Added initial SQLAlchemy user and daily wearable metric models with database constraints, relationship and SQLite schema regression tests |
| Day 23 | 2 Nov 2026 | Added Alembic migration configuration and initial schema revision with rollback; generated PostgreSQL upgrade SQL successfully for offline review |
| Day 24 | 2 Nov 2026 | Made the API start without a missing model artifact, added repeatable Isolation Forest training, packaged the trained artifact, added readiness checks, environment-configured CORS and endpoint regression tests |
| Day 25 | 2 Nov 2026 | Added production HTTPS CORS allowlist validation, security response headers, sanitized validation errors, non-finite prediction input rejection and regression tests |
| Day 26 | 2 Nov 2026 | Added responsive browser dashboard for baseline deviations, API status, research-safe result interpretation and same-origin serving through FastAPI |
| Day 27 | 2 Nov 2026 | Added citation-backed retrieval over reviewed CDC activity and sleep guidance, `/api/v1/ask`, extractive fallback and optional local Ollama generation with no paid API requirement |
| Day 28 | 2 Nov 2026 | Added modular data-quality, activity-trend and sleep-trend agents coordinated through a validated 14–60-day workflow and existing research model |
| Day 29 | 2 Nov 2026 | Added non-root Docker image, Render Blueprint with managed PostgreSQL, startup migrations, production readiness checks and GitHub Actions CI |
| Day 30 | 2 Nov 2026 | GitHub Actions passed tests, PostgreSQL migration SQL generation and Docker image build; adjusted startup migrations for Render free-tier compatibility. Public service creation and health-check verification remain |

## Run locally

Install the declared application dependencies with `python -m pip install .`, copy `.env.example` to `.env`, and set the local PostgreSQL values. Start the API and dashboard with `python -m uvicorn backend.main:app --reload`. Apply schema changes with `python -m alembic upgrade head`.

## Public prototype deployment

The Docker image and `render.yaml` are configured for a public educational prototype. In Render, create a Blueprint from this repository and review the generated web service and PostgreSQL resources before confirming. The container applies database migrations before starting the API, then checks `/api/v1/ready`. The service does not require a paid model API; optional local Ollama generation is disabled unless configured.

The included Render plans are free-tier demo settings. Render documents that free web services are not for production use and that free PostgreSQL databases expire 30 days after creation; do not use this setup for long-term or real health records. Upgrade the database plan and complete a privacy/security review before storing any personal data.
