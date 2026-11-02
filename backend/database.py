import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load environment variables
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

# Prefer a managed DATABASE_URL, with individual DB_* variables for local use.
configured_url = os.getenv("DATABASE_URL")
if configured_url:
    parsed_url = make_url(configured_url)
    DATABASE_URL = (
        parsed_url.set(drivername="postgresql+psycopg")
        if parsed_url.drivername == "postgresql"
        else parsed_url
    )
else:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5433")),
        database=os.getenv("DB_NAME"),
    )

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Create database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    """Base class for the application's SQLAlchemy models."""
