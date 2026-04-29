from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    booked_at: Mapped[date] = mapped_column(Date, index=True)
    type: Mapped[TransactionType] = mapped_column(SqlEnum(TransactionType), index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
