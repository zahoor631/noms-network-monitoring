from sqlalchemy.orm import Session
from app.models.alert import Alert, AlertSeverity
from app.schemas.alert import AlertCreate


def create_alert(db: Session, payload: AlertCreate) -> Alert:
    alert = Alert(**payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def resolve_alert(db: Session, alert_id: int) -> Alert:
    from datetime import datetime, timezone
    alert = db.query(Alert).get(alert_id)
    if alert:
        alert.is_resolved = True
        alert.resolved_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(alert)
    return alert