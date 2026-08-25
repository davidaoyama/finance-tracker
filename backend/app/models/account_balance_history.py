from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AccountBalanceHistory(Base):
    __tablename__ = "account_balance_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )