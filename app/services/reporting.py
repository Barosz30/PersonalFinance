from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction, TransactionType
from app.schemas.report import CategorySpend, MonthlyReport


def build_monthly_report(db: Session, user_id: int, year: int, month: int) -> MonthlyReport:
    start = date(year, month, 1)
    end = date(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)

    base_filters = [
        Transaction.booked_at >= start,
        Transaction.booked_at < end,
        Transaction.account_id.in_(select(Account.id).where(Account.user_id == user_id)),
    ]
    income = db.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            *base_filters, Transaction.type == TransactionType.income
        )
    )
    expense = db.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            *base_filters, Transaction.type == TransactionType.expense
        )
    )
    top = db.execute(
        select(Category.name, func.sum(Transaction.amount))
        .join(Category, Category.id == Transaction.category_id, isouter=True)
        .where(*base_filters, Transaction.type == TransactionType.expense)
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(5)
    ).all()
    top_categories = [CategorySpend(category=row[0] or "Uncategorized", amount=row[1]) for row in top]

    total_income = Decimal(str(income))
    total_expense = Decimal(str(expense))
    return MonthlyReport(
        year=year,
        month=month,
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        top_categories=top_categories,
    )
