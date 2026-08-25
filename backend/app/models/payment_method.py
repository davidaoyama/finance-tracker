from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

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

    funding_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
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