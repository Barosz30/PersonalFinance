from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryPublic

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryPublic])
def list_categories(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[CategoryPublic]:
    categories = db.scalars(select(Category).where(Category.user_id == user.id)).all()
    return [CategoryPublic.model_validate(item) for item in categories]


@router.post("", response_model=CategoryPublic, status_code=201)
def create_category(
    payload: CategoryCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> CategoryPublic:
    category = Category(name=payload.name, user_id=user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryPublic.model_validate(category)
