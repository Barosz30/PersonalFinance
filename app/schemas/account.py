from decimal import Decimal

from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str
    balance: Decimal = Decimal("0")


class AccountPublic(AccountCreate):
    id: int

    model_config = {"from_attributes": True}
