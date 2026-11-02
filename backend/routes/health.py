from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from backend.database import engine
from backend.services.model_service import model_is_available

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Health-AI"
    }


@router.get("/ready")
def readiness_check():
    checks = {"model": model_is_available(), "database": False}
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception:
        pass
    ready = all(checks.values())
    return JSONResponse(
        status_code=200 if ready else 503,
        content={"status": "ready" if ready else "not_ready", "checks": checks},
    )
@router.get("/")
def root():
    return {"message": "Health-AI API is running"}
