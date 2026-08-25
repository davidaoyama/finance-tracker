from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    memo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Used for expenses and income.
    account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True,
    )

    # Used for transfers.
    source_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True,
    )

    # Used for transfers.
    destination_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True,
    )

    # Used for expenses.
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )

    # Used for expenses.
    payment_method_id: Mapped[int | None] = mapped_column(
        ForeignKey("payment_methods.id"),
        nullable=True,
    )

    # Only populated when a reward rule applies.
    points_multiplier: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2),
        nullable=True,
    )

    points_earned: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )