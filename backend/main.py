from fastapi import FastAPI
from backend.routes import health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Health-AI",
    description="AI-powered personalized health platform",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health.router,
    prefix="/api/v1"
)