from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryPublic(CategoryCreate):
    id: int

    model_config = {"from_attributes": True}
