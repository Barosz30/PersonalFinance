from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.budget import Budget
from app.models.category import Category
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetPublic

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("", response_model=list[BudgetPublic])
def list_budgets(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[BudgetPublic]:
    budgets = db.scalars(select(Budget).where(Budget.user_id == user.id)).all()
    return [BudgetPublic.model_validate(item) for item in budgets]


@router.post("", response_model=BudgetPublic, status_code=201)
def upsert_budget(
    payload: BudgetCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> BudgetPublic:
    _ = db.scalar(select(Category).where(Category.id == payload.category_id, Category.user_id == user.id))
    existing = db.scalar(
        select(Budget).where(
            Budget.user_id == user.id,
            Budget.category_id == payload.category_id,
            Budget.year == payload.year,
            Budget.month == payload.month,
        )
    )
    if existing is None:
        existing = Budget(user_id=user.id, **payload.model_dump())
        db.add(existing)
    else:
        existing.limit_amount = payload.limit_amount
    db.commit()
    db.refresh(existing)
    return BudgetPublic.model_validate(existing)
