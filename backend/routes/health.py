from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Health-AI"
    }
@router.get("/")
def root():
    return {"message": "Health-AI API is running"}