from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class GoalContribution(Base):
    __tablename__ = "goal_contributions"

    id: Mapped[int] = mapped_column(primary_key=True)

    goal_id: Mapped[int] = mapped_column(
        ForeignKey("goals.id"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True,
    )

    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )