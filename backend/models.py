from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class User(Base):
    """Research prototype account used to scope wearable observations."""

    __tablename__ = "users"
    __table_args__ = (Index("ix_users_email", "email", unique=True),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    daily_metrics: Mapped[list["DailyHealthMetric"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class DailyHealthMetric(Base):
    """Daily wearable summary; values are observational, not diagnostic."""

    __tablename__ = "daily_health_metrics"
    __table_args__ = (
        UniqueConstraint("user_id", "observed_on", name="uq_daily_metric_user_date"),
        CheckConstraint("steps >= 0", name="ck_daily_metric_steps_nonnegative"),
        CheckConstraint(
            "sleep_hours >= 0 AND sleep_hours <= 24", name="ck_daily_metric_sleep_range"
        ),
        CheckConstraint(
            "resting_heart_rate IS NULL OR resting_heart_rate > 0",
            name="ck_daily_metric_heart_rate_positive",
        ),
        Index("ix_daily_metric_user_date", "user_id", "observed_on"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    observed_on: Mapped[date] = mapped_column(Date, nullable=False)
    steps: Mapped[int] = mapped_column(Integer, nullable=False)
    sleep_hours: Mapped[float] = mapped_column(Float, nullable=False)
    resting_heart_rate: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user: Mapped[User] = relationship(back_populates="daily_metrics")
