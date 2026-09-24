from pydantic import BaseModel
from datetime import datetime
from app.models.alert import AlertSeverity


class AlertBase(BaseModel):
    device_id: int | None = None
    severity: AlertSeverity = AlertSeverity.info
    title: str
    message: str | None = None


class AlertCreate(AlertBase):
    pass


class AlertOut(AlertBase):
    id: int
    is_resolved: bool
    created_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True