from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    target_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    current_allocated_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    linked_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True,
    )

    frequency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    target_date: Mapped[date | None] = mapped_column(
        Date,
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