from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import Token, UserCreate, UserPublic
from app.services.auth import login_for_token, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserPublic:
    user = register_user(db, payload)
    return UserPublic.model_validate(user)


@router.post("/token", response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    token_value = login_for_token(db, form_data.username, form_data.password)
    return Token(access_token=token_value)
