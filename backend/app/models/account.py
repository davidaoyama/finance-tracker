from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # decimal type better for arithmetic operations and avoids floating-point precision issues
    current_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
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

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )