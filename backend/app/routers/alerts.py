from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.alert import Alert, AlertSeverity
from app.schemas.alert import AlertCreate, AlertOut
from app.core.dependencies import get_current_user, admin_or_engineer
from app.services import alert_service

router = APIRouter()


@router.get("/", response_model=List[AlertOut])
def list_alerts(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
    severity: Optional[AlertSeverity] = None,
    resolved: Optional[bool] = None,
):
    q = db.query(Alert)
    if severity:
        q = q.filter(Alert.severity == severity)
    if resolved is not None:
        q = q.filter(Alert.is_resolved == resolved)
    return q.order_by(Alert.created_at.desc()).all()


@router.post("/", response_model=AlertOut, dependencies=[Depends(admin_or_engineer)])
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    return alert_service.create_alert(db, payload)


@router.post("/{alert_id}/resolve", response_model=AlertOut, dependencies=[Depends(admin_or_engineer)])
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = alert_service.resolve_alert(db, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    return alert