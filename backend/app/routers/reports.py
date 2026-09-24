from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.services import report_service

router = APIRouter()


@router.get("/uptime")
def uptime(
    days: int = Query(1, ge=1, le=30),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return report_service.uptime_report(db, days=days)


@router.get("/incidents")
def incidents(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return report_service.incident_report(db)


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return report_service.dashboard_summary(db)