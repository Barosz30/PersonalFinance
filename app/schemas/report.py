from decimal import Decimal

from pydantic import BaseModel


class CategorySpend(BaseModel):
    category: str
    amount: Decimal


class MonthlyReport(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    top_categories: list[CategorySpend]
