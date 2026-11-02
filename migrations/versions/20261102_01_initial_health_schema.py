"""Create initial user and daily wearable metric tables."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20261102_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "daily_health_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("observed_on", sa.Date(), nullable=False),
        sa.Column("steps", sa.Integer(), nullable=False),
        sa.Column("sleep_hours", sa.Float(), nullable=False),
        sa.Column("resting_heart_rate", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("user_id", "observed_on", name="uq_daily_metric_user_date"),
        sa.CheckConstraint("steps >= 0", name="ck_daily_metric_steps_nonnegative"),
        sa.CheckConstraint(
            "sleep_hours >= 0 AND sleep_hours <= 24", name="ck_daily_metric_sleep_range"
        ),
        sa.CheckConstraint(
            "resting_heart_rate IS NULL OR resting_heart_rate > 0",
            name="ck_daily_metric_heart_rate_positive",
        ),
    )
    op.create_index(
        "ix_daily_metric_user_date", "daily_health_metrics", ["user_id", "observed_on"]
    )


def downgrade() -> None:
    op.drop_index("ix_daily_metric_user_date", table_name="daily_health_metrics")
    op.drop_table("daily_health_metrics")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
