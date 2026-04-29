from fastapi import FastAPI

from app.api.routes.accounts import router as accounts_router
from app.api.routes.auth import router as auth_router
from app.api.routes.budgets import router as budgets_router
from app.api.routes.categories import router as categories_router
from app.api.routes.health import router as health_router
from app.api.routes.reports import router as reports_router
from app.api.routes.transactions import router as transactions_router
from app.db.base import Base
from app.db.session import engine
from app.models import account, budget, category, transaction, user  # noqa: F401

app = FastAPI(title="Personal Finance API", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(budgets_router)
app.include_router(reports_router)
