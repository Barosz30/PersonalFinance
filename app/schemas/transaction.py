from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal
    note: str | None = None
    booked_at: date
    type: TransactionType
    account_id: int
    category_id: int | None = None


class TransactionPublic(TransactionCreate):
    id: int

    model_config = {"from_attributes": True}
