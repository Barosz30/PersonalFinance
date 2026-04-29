import csv
from io import StringIO

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.report import MonthlyReport
from app.services.reporting import build_monthly_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly", response_model=MonthlyReport)
def monthly_report(
    year: int = Query(..., ge=2000, le=2200),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MonthlyReport:
    return build_monthly_report(db, user.id, year, month)


@router.get("/monthly/csv")
def monthly_report_csv(
    year: int = Query(..., ge=2000, le=2200),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> StreamingResponse:
    report = build_monthly_report(db, user.id, year, month)
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["year", "month", "total_income", "total_expense", "balance"])
    writer.writerow([report.year, report.month, report.total_income, report.total_expense, report.balance])
    writer.writerow([])
    writer.writerow(["top_category", "amount"])
    for item in report.top_categories:
        writer.writerow([item.category, item.amount])
    buffer.seek(0)
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv")
