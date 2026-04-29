from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountPublic

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountPublic])
def list_accounts(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[AccountPublic]:
    accounts = db.scalars(select(Account).where(Account.user_id == user.id)).all()
    return [AccountPublic.model_validate(item) for item in accounts]


@router.post("", response_model=AccountPublic, status_code=201)
def create_account(
    payload: AccountCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> AccountPublic:
    account = Account(name=payload.name, balance=payload.balance, user_id=user.id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return AccountPublic.model_validate(account)


@router.get("/{account_id}", response_model=AccountPublic)
def get_account(
    account_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> AccountPublic:
    account = db.scalar(select(Account).where(Account.id == account_id, Account.user_id == user.id))
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return AccountPublic.model_validate(account)
