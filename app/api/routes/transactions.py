from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionPublic

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionPublic])
def list_transactions(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[TransactionPublic]:
    account_ids = select(Account.id).where(Account.user_id == user.id)
    items = db.scalars(select(Transaction).where(Transaction.account_id.in_(account_ids))).all()
    return [TransactionPublic.model_validate(item) for item in items]


@router.post("", response_model=TransactionPublic, status_code=201)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TransactionPublic:
    account = db.scalar(select(Account).where(Account.id == payload.account_id, Account.user_id == user.id))
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    if payload.category_id is not None:
        category = db.scalar(select(Category).where(Category.id == payload.category_id, Category.user_id == user.id))
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return TransactionPublic.model_validate(transaction)
