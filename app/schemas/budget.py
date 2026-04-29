from decimal import Decimal

from pydantic import BaseModel, Field


class BudgetCreate(BaseModel):
    category_id: int
    year: int = Field(ge=2000, le=2200)
    month: int = Field(ge=1, le=12)
    limit_amount: Decimal


class BudgetPublic(BudgetCreate):
    id: int

    model_config = {"from_attributes": True}
