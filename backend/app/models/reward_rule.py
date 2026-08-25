from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class RewardRule(Base):
    __tablename__ = "reward_rules"

    id: Mapped[int] = mapped_column(primary_key=True)

    payment_method_id: Mapped[int] = mapped_column(
        ForeignKey("payment_methods.id"),
        nullable=False,
    )

    # NULL means the default/catch-all rule.
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )

    multiplier: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
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