from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database import Base
from backend.models import DailyHealthMetric, User


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    engine.dispose()


def test_user_and_daily_metric_round_trip(session):
    user = User(email="researcher@example.test")
    user.daily_metrics.append(
        DailyHealthMetric(
            observed_on=date(2026, 11, 2),
            steps=7200,
            sleep_hours=7.5,
            resting_heart_rate=62,
        )
    )
    session.add(user)
    session.commit()

    saved = session.query(DailyHealthMetric).one()
    assert saved.user.email == "researcher@example.test"
    assert saved.steps == 7200
    assert saved.sleep_hours == 7.5


def test_daily_metric_rejects_negative_steps(session):
    user = User(email="invalid@example.test")
    session.add(user)
    session.flush()
    session.add(
        DailyHealthMetric(
            user_id=user.id,
            observed_on=date(2026, 11, 2),
            steps=-1,
            sleep_hours=7,
        )
    )
    with pytest.raises(IntegrityError):
        session.commit()


def test_email_is_unique(session):
    session.add_all(
        [User(email="same@example.test"), User(email="same@example.test")]
    )
    with pytest.raises(IntegrityError):
        session.commit()
